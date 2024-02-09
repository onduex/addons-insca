from odoo import fields, models, api, _


class Subconjunto(models.Model):
    _name = 'subconjunto'
    _description = 'subconjunto'
    name = fields.Char(string="Name", required=True)


class Seccion(models.Model):
    _name = 'seccion'
    _description = 'seccion'
    name = fields.Char(string="Name", required=True)


class Material(models.Model):
    _name = 'material'
    _description = 'material'
    name = fields.Char(string="Name", required=True)


class Acabado(models.Model):
    _name = 'acabado'
    _description = 'acabado'
    name = fields.Char(string="Name", required=True)


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    subconjunto = fields.Many2one(comodel_name="subconjunto", string="Subconjunto",
                                  required=False,
                                  store=True,
                                  default=lambda self: self.env['subconjunto'].search([('name', '=', '#')]))
    seccion = fields.Many2one(comodel_name="seccion", string="Seccion",
                              required=False,
                              store=True,
                              default=lambda self: self.env['seccion'].search([('name', '=', '#')]))
    entregado = fields.Boolean(string='Entregado', required=False, store=True, default=False)
    recibido = fields.Boolean(string='Recibido', required=False, store=True, default=False)
    n_pedido_compras = fields.Char(string='Gestwin', required=False, store=True)
    fecha_solicitud = fields.Date(string='F. solicitud', required=False, related='bom_id.fecha_solicitud', store=True)
    fecha_recepcion = fields.Date(string='F. recepción', required=False, related='bom_id.fecha_recepcion', store=True)
    fecha_entrega_cliente = fields.Date(string='F. entrega cliente', required=False,
                                        related='bom_id.fecha_entrega_cliente', store=True)
    trabajo = fields.Many2one(comodel_name='project.project', string='Trabajo',
                              required=False, related='bom_id.trabajo', store=True)
    cliente = fields.Many2one(comodel_name='res.partner', string='Cliente',
                              required=False, related='bom_id.cliente', store=True)
    emitido = fields.Many2one(comodel_name='hr.employee', string='Emitido por',
                              required=False, related='bom_id.emitido', store=True)
    recibido_por = fields.Many2one(comodel_name='hr.employee', string='Recibido por', required=False)
    product_name = fields.Char(string='Nombre', related='product_tmpl_id.name', store=True)
    product_default_code = fields.Char(string='Referencia', related='product_tmpl_id.default_code', store=True)

    @api.depends('product_id', 'product_id.material', 'product_id.acabado')
    @api.onchange('product_id')
    def _onchange_product_id(self):
        for rec in self:
            if rec.product_id:
                rec.material = rec.product_id.material.name
                rec.acabado = rec.product_id.acabado.name

    material = fields.Char(string="Material", required=False, store=True, compute=_onchange_product_id)
    acabado = fields.Char(string="Acabado", required=False, store=True, compute=_onchange_product_id)

    @staticmethod
    def list_customers(docs):
        lst_customers = []
        str_customer = ''
        for record in docs:
            if record.cliente.name not in lst_customers:
                lst_customers.append(record.cliente.name)
        if len(lst_customers) == 1:
            str_customer = lst_customers[0]
        if len(lst_customers) > 1:
            for customer in lst_customers:
                str_customer = str_customer + " - " + customer
        return str_customer

    @staticmethod
    def list_works(docs):
        lst_works = []
        str_work = ''
        for record in docs:
            if record.trabajo.name not in lst_works:
                lst_works.append(record.trabajo.name)
        if len(lst_works) == 1:
            str_work = lst_works[0]
        if len(lst_works) > 1:
            for work in lst_works:
                str_work = str_work + " - " + work
        return str_work

    @staticmethod
    def list_managers(docs):
        lst_managers = []
        str_manager = ''
        for record in docs:
            if record.emitido.name not in lst_managers:
                lst_managers.append(record.emitido.name)
        if len(lst_managers) == 1:
            str_manager = lst_managers[0]
        if len(lst_managers) > 1:
            for manager in lst_managers:
                str_manager = str_manager + " - " + manager
        return str_manager

    @staticmethod
    def list_solicitudes(docs):
        lst_solicitudes = []
        str_solicitud = ''
        for record in docs:
            if record.fecha_solicitud not in lst_solicitudes:
                lst_solicitudes.append(record.fecha_solicitud)
        if len(lst_solicitudes) == 1:
            str_solicitud = lst_solicitudes[0]
        if len(lst_solicitudes) > 1:
            for solicitud in lst_solicitudes:
                str_solicitud = str_solicitud + " - " + solicitud
        return str_solicitud

    @staticmethod
    def list_recepciones(docs):
        lst_recepciones = []
        str_recepcion = ''
        for record in docs:
            if record.fecha_recepcion not in lst_recepciones:
                lst_recepciones.append(record.fecha_recepcion)
        if len(lst_recepciones) == 1:
            str_recepcion = lst_recepciones[0]
        if len(lst_recepciones) > 1:
            for recepcion in lst_recepciones:
                str_recepcion = str_recepcion + " - " + recepcion
        return str_recepcion

    @staticmethod
    def list_entregas(docs):
        lst_entregas = []
        str_entrega = ''
        for record in docs:
            if record.fecha_entrega_cliente not in lst_entregas:
                lst_entregas.append(record.fecha_entrega_cliente)
        if len(lst_entregas) == 1:
            str_entrega = lst_entregas[0]
        if len(lst_entregas) > 1:
            for entrega in lst_entregas:
                str_entrega = str_entrega + " - " + entrega
        return str_entrega
