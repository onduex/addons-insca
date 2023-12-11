# -*- coding: utf-8 -*-
# © 2023 Tomás Pascual (<tompascual@outlook.es>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _
from odoo.exceptions import CacheMiss
from smb.SMBConnection import SMBConnection
from odoo.exceptions import ValidationError
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import tempfile
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger
import PyPDF2
import pprint
from datetime import datetime


pp = pprint.PrettyPrinter(indent=4)
lines = []


class PrintBomWiz(models.TransientModel):
    _name = 'print.bom.wiz'
    _description = 'Wizard para imprimir LdM'

    button_pressed = fields.Char(string='Solicitud', required=False, readonly=True, default='')
    completa = fields.Boolean(string='Completa', required=False, default=False)
    herrajes = fields.Boolean(string='Herrajes', required=False, default=False)
    madera = fields.Boolean(string='Madera', required=False, default=False)
    pantografo = fields.Boolean(string='Pantografo', required=False, default=False)
    metal = fields.Boolean(string='Metal', required=False, default=False)
    pdf_link = fields.Char(string='PDF Link', required=False, store=True)

    bom_id = fields.Many2one(comodel_name='mrp.bom',
                             string="Lista de materiales",
                             readonly=False, ondelete="cascade")

    bom_line_ids = fields.One2many(
        comodel_name='print.bom.line',
        inverse_name='id',
        string='Componente',
        required=False,
    )

    def print_all_bom_children_with_bom(self, ch, row, level):
        i, j = row, level
        j += 1
        line = (0, 0, {'to_print': True,
                       'mrp_bom_line_level': ("- - " * j) + ch.product_id.default_code,
                       'default_code': ch.product_id.default_code,
                       'name': ch.product_id.name,
                       'qty': ch.product_qty,
                       'has_bom_line_ids': len(ch.child_line_ids),
                       'route': ch.child_bom_id.vault_route or None,
                       'path': str(ch.product_id.png_link)[19:].strip().replace('png', 'pdf').
                replace('0_PNG', '1_PDF') or None,
                       'parent_bom': ch.bom_id.product_tmpl_id.default_code or None,
                       'wizard_id': self.id,
                       })
        if line[2]['has_bom_line_ids'] != 0:
            lines.append(line)
        try:
            for child in ch.child_line_ids:
                i = self.print_all_bom_children_with_bom(child, i, j)

        except CacheMiss:
            # The Bom has no childs, thus it is the last level.
            # When a BoM has no childs, child_line_ids is None, this creates a
            # CacheMiss Error. However, this is expected because there really
            # cannot be child_line_ids.
            pass

        j -= 1
        return lines

    def get_all_bom_lines_with_bom(self):
        files_to_merge = []
        self.remove_bom_lines()
        res_company_obj = self.env['res.company'].search([('id', '=', self.env.user.company_id.id)])
        conn = self.establish_conn()

        i = 0
        for o in self.bom_id:
            i += 1
            j = 0
            for ch in o.bom_line_ids:
                i = self.print_all_bom_children_with_bom(ch, i, j)

        line_0 = (0, 0, {'to_print': True,
                         'mrp_bom_line_level': self.bom_id.product_tmpl_id.default_code,
                         'default_code': self.bom_id.product_tmpl_id.default_code,
                         'name': self.bom_id.product_tmpl_id.name,
                         'qty': 1,
                         'has_bom_line_ids': len(self.bom_id.bom_line_ids),
                         'route': self.bom_id.vault_route or None,
                         'path': str(self.bom_id.product_tmpl_id.png_link)[19:].strip().replace('png', 'pdf').
                  replace('0_PNG', '1_PDF') or None,
                         'parent_bom': None,
                         'wizard_id': self.id,
                         })
        i = [line_0] + i
        for line in i:
            remote_file = ('/' + res_company_obj.filestore_server_shared_folder_level1_3 + '/' + line[2]['path'])
            files_to_merge.append(remote_file)
            try:
                file_obj = tempfile.NamedTemporaryFile()
                file_attributes, filesize = conn.retrieveFile(res_company_obj.filestore_server_shared_folder_3,
                                                              remote_file, file_obj, timeout=30)
                if filesize:
                    line[2]['has_pdf'] = True
                file_obj.close()

            except Exception as e:
                if e:
                    string = str(' | ') + str(line[2]['default_code'])
                    self.button_pressed += string
        conn.close()
        context = {'default_bom_id': self.bom_id.id,
                   'default_bom_line_ids': [line_0] + lines,
                   'default_button_pressed': self.button_pressed,
                   'default_completa': True,
                   'default_herrajes': True,
                   'default_madera': True,
                   'default_pantografo': True,
                   'default_metal': True
                   }
        return {
            'name': 'Imprimir Lista de Materiales',
            'type': 'ir.actions.act_window',
            'res_model': 'print.bom.wiz',
            'context': context,
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': 3023,
            'target': 'new'}

    def get_lists(self):
        list_completa = []
        list_herrajes = []
        list_madera = []
        list_pantografo = []
        list_metal = []
        list_metal_to_postprocessor = []
        list_metal_postprocessing = []
        if self.bom_line_ids:
            for rec in self.bom_line_ids:
                list_completa.append(rec.id)
                if rec['default_code'][0:4] == 'A70.' or rec['default_code'][0:4] == 'A72.':
                    list_herrajes.append(rec.id)
                if rec['default_code'][0:4] == 'A10.' or rec['default_code'][0:4] == 'A11.':
                    list_madera.append(rec.id)
                if (rec['route'] and 'PTG' in rec['route'] and
                        (rec['default_code'][0:4] == 'A10.' or rec['default_code'][0:4] == 'A11.')):
                    list_pantografo.append(rec.id)

                if rec['parent_bom'] and rec['parent_bom'][0:4] == 'A31.':
                    pass
                elif rec['parent_bom'] and rec['parent_bom'][0:4] == 'A30.' and rec['default_code'][0:4] == 'A30.':
                    pass
                elif rec['default_code'][0:4] == 'A70.' \
                        or rec['default_code'][0:4] == 'A10.' \
                        or rec['default_code'][0:4] == 'A11.' \
                        or rec['default_code'][0:4] == 'A12.' \
                        or rec['default_code'][0:4] == 'A15.':
                    pass
                elif rec['default_code'][0:4] == 'A00.':
                    pass
                else:
                    list_metal.append(rec.id)
                    list_metal_to_postprocessor.append(rec)

            for record in list_metal_to_postprocessor:
                if record['parent_bom'] and record['parent_bom'][0:4] != 'A00.':
                    if (record['default_code'][0:4] == 'A30.' or record['default_code'][0:4] == 'A31.') and \
                            (record['parent_bom'][0:4] != 'A31.' or record['parent_bom'][0:4] != 'A32.'):
                        if record['parent_bom'] not in list_metal_postprocessing:
                            list_metal_postprocessing.append(record['parent_bom'])

            for rec2 in self.bom_line_ids:
                if rec2['default_code'] in list_metal_postprocessing:
                    list_metal.append(rec2.id)

        return [list_completa, list_herrajes, list_madera, list_pantografo, list_metal]

    @api.onchange('completa')
    def onchange_completa(self):
        lists = self.get_lists()
        if not self.completa:
            self.herrajes = False
            self.madera = False
            self.pantografo = False
            self.metal = False
            for line in self.bom_line_ids:
                if line.id in lists[0]:
                    line.to_print = False
        if self.completa:
            self.herrajes = True
            self.madera = True
            self.pantografo = True
            self.metal = True
            for line in self.bom_line_ids:
                if line.id in lists[0]:
                    line.to_print = True

    @api.onchange('herrajes')
    def onchange_herrajes(self):
        lists = self.get_lists()
        if not self.herrajes:
            for line in self.bom_line_ids:
                if line.id in lists[1]:
                    line.to_print = False
        if self.herrajes:
            for line in self.bom_line_ids:
                if line.id in lists[1]:
                    line.to_print = True

    @api.onchange('madera')
    def onchange_madera(self):
        lists = self.get_lists()
        if not self.madera:
            self.pantografo = False
            for line in self.bom_line_ids:
                if line.id in lists[2]:
                    line.to_print = False
        if self.madera:
            self.pantografo = True
            for line in self.bom_line_ids:
                if line.id in lists[2]:
                    line.to_print = True

    @api.onchange('pantografo')
    def onchange_pantografo(self):
        lists = self.get_lists()
        if not self.pantografo:
            for line in self.bom_line_ids:
                if line.id in lists[3]:
                    line.to_print = False
        if self.pantografo:
            for line in self.bom_line_ids:
                if line.id in lists[3]:
                    line.to_print = True

    @api.onchange('metal')
    def onchange_metal(self):
        lists = self.get_lists()
        if not self.metal:
            for line in self.bom_line_ids:
                if line.id in lists[4]:
                    line.to_print = False
        if self.metal:
            lists[4].append(self.bom_line_ids[0].id)
            for line in self.bom_line_ids:
                if line.id in lists[4]:
                    line.to_print = True

    def establish_conn(self):
        res_company_obj = self.env['res.company'].search([('id', '=', self.env.user.company_id.id)])
        conn = SMBConnection(res_company_obj.smb_user,
                             res_company_obj.smb_pass,
                             res_company_obj.odoo_server_name,
                             res_company_obj.filestore_server_name,
                             use_ntlm_v2=True
                             )
        conn.connect(res_company_obj.filestore_server_ip,
                     res_company_obj.filestore_server_port
                     )
        return conn

    def remove_bom_lines(self):
        lines.clear()
        self.button_pressed = ''
        context = {'default_bom_id': self.bom_id.id,
                   'default_bom_line_ids': lines}
        return {
            'name': 'Imprimir Lista de Materiales',
            'type': 'ir.actions.act_window',
            'res_model': 'print.bom.wiz',
            'context': context,
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': 3023,
            'target': 'new'}

    def print_bom(self):
        mergeFile = PyPDF2.PdfFileMerger()
        writerFile = PyPDF2.PdfFileWriter()
        files_to_merge = []
        files_to_merge2 = []
        conn = self.establish_conn()
        res_company_obj = self.env['res.company'].search([('id', '=', self.env.user.company_id.id)])
        wizard_ids = self.env.context.get('active_ids', [])

        impLine = self.env['print.bom.line'].search([('wizard_id', '=', wizard_ids[0])])

        for rec in impLine:
            if rec.to_print and rec.has_pdf:
                files_to_merge.append(rec.path)
            elif not rec.to_print and not rec.has_pdf:
                continue
            else:
                raise ValidationError(_("No está permitido tener seleccionado el check de impresión y "
                                        "que haya ausencia de PDF: ") + str(rec.default_code))

        for file_path in files_to_merge:
            remote_file = ('/' + res_company_obj.filestore_server_shared_folder_level1_3 + '/' + file_path)
            local_file = '/tmp/' + remote_file[remote_file.rfind('/'):][1:]
            try:
                with open(local_file, 'wb') as file_obj:
                    conn.retrieveFile(res_company_obj.filestore_server_shared_folder_3, remote_file, file_obj,
                                      timeout=30)
                    files_to_merge2.append(local_file)
            except Exception as e:
                if e:
                    raise ValidationError(_("No se ha podido descargar el archivo: ") + str(file_path))

        for pdf in files_to_merge2:
            mergeFile.append(PyPDF2.PdfFileReader(open(pdf, 'rb')))
        local_file_to_remote = '/tmp/' + files_to_merge2[0][files_to_merge2[0].rfind('/'):][1:]
        mergeFile.write(local_file_to_remote)

        pdf_enumerado = PyPDF2.PdfFileReader(local_file_to_remote)

        for page in range(pdf_enumerado.getNumPages()):
            current_dateTime = datetime.now()
            packet = io.BytesIO()
            can = canvas.Canvas(packet, pagesize=A4)
            can.drawRightString(818, 10, current_dateTime.strftime("%d-%m-%Y - %H:%M:%S") + ' - ' +
                                files_to_merge2[0][files_to_merge2[0].rfind('/'):][1:][:-4] + ' - ' +
                                str(page + 1) + ' / ' + str(pdf_enumerado.getNumPages()))  # add page number
            can.save()
            packet.seek(0)
            watermark = PdfFileReader(packet)
            watermark_page = watermark.getPage(0)
            pdf_page = pdf_enumerado.getPage(page)
            pdf_page.mergePage(watermark_page)
            writerFile.addPage(pdf_page)

        with open(local_file_to_remote, 'wb') as fh:
            writerFile.write(fh)

        try:
            remote_file_write_back = ('/DTECNIC/PLANOS/TMP_PDF/' + local_file_to_remote[5:])
            with open(local_file_to_remote, 'rb') as file_obj:
                conn.storeFile(res_company_obj.filestore_server_shared_folder_3, remote_file_write_back, file_obj,
                               timeout=30)
                self.pdf_link = remote_file_write_back
        except Exception as e:
            if e:
                raise ValidationError(_("No se ha podido subir el archivo: ") + str(local_file_to_remote))
        conn.close()

        context = {'default_bom_id': self.bom_id.id}
        return {
            'name': 'Imprimir Lista de Materiales',
            'type': 'ir.actions.act_window',
            'res_model': 'print.bom.wiz',
            'context': context,
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': 3023,
            'target': 'new'}
