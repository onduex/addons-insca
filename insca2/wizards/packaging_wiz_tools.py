# -*- coding: utf-8 -*-
# © 2019 Sergio Díaz (<sdimar@yahoo.com>).
# License GPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class CreatePackagingWiz(models.TransientModel):
    _inherit = 'create.packaging.wiz'

    # Tapa
    @staticmethod
    def get_major_dimension_type_one(largo, ancho, espesorg):
        if largo > ancho:
            res = 'PIEZA EMBALAJE ' + str(largo).zfill(4) + 'x' + str(ancho).zfill(4) + 'x' + \
                  str(espesorg).zfill(3) + 'mm'
        else:
            res = 'PIEZA EMBALAJE ' + str(ancho).zfill(4) + 'x' + str(largo).zfill(4) + 'x' + \
                  str(espesorg).zfill(3) + 'mm'
        return res

    # Base
    @staticmethod
    def get_major_dimension_type_two(largo, ancho, espesorb):
        if largo > ancho:
            res = 'PIEZA EMBALAJE ' + str(largo).zfill(4) + 'x' + str(ancho).zfill(4) + 'x' + \
                  str(espesorb).zfill(3) + 'mm'
        else:
            res = 'PIEZA EMBALAJE ' + str(ancho).zfill(4) + 'x' + str(largo).zfill(4) + 'x' + \
                  str(espesorb).zfill(3) + 'mm'
        return res

    # Lateral largo
    @staticmethod
    def get_major_dimension_type_three(largo, alto, espesorg, alto_tacos, espesorb, distancia_suelo, tipo_palet):
        res = ''
        if tipo_palet == '1':
            a = int(largo) + (2 * int(espesorg)) + 1
            b = int(alto) + int(alto_tacos) - int(distancia_suelo)
            if largo > alto:
                res = 'PIEZA EMBALAJE ' + str(a).zfill(4) + 'x' + str(b).zfill(4) + 'x' + \
                      str(espesorg).zfill(3) + 'mm'
            else:
                res = 'PIEZA EMBALAJE ' + str(b).zfill(4) + 'x' + str(a).zfill(4) + 'x' + \
                      str(espesorg).zfill(3) + 'mm'
        elif tipo_palet == '0':
            a = int(largo) + (2 * int(espesorg)) + 1
            b = int(alto) + int(alto_tacos) - int(alto_tacos)
            if largo > alto:
                res = 'PIEZA EMBALAJE ' + str(a).zfill(4) + 'x' + str(b).zfill(4) + 'x' + \
                      str(espesorg).zfill(3) + 'mm'
            else:
                res = 'PIEZA EMBALAJE ' + str(b).zfill(4) + 'x' + str(a).zfill(4) + 'x' + \
                      str(espesorg).zfill(3) + 'mm'
        elif tipo_palet == '4' or tipo_palet == '5':
            a = int(largo) + (2 * int(espesorg)) + 1
            b = int(alto) + int(espesorb)
            if largo > alto:
                res = 'PIEZA EMBALAJE ' + str(a).zfill(4) + 'x' + str(b).zfill(4) + 'x' + \
                      str(espesorg).zfill(3) + 'mm'
            else:
                res = 'PIEZA EMBALAJE ' + str(b).zfill(4) + 'x' + str(a).zfill(4) + 'x' + \
                      str(espesorg).zfill(3) + 'mm'
        return res

    # Lateral corto
    @staticmethod
    def get_major_dimension_type_four(alto, ancho, espesorg, tipo_palet, espesorb, alto_tacos):
        if tipo_palet != '4' and tipo_palet != '5':
            if alto > ancho:
                res = 'PIEZA EMBALAJE ' + str(alto).zfill(4) + 'x' + str(ancho).zfill(4) + 'x' + \
                      str(espesorg).zfill(3) + 'mm'
            else:
                res = 'PIEZA EMBALAJE ' + str(ancho).zfill(4) + 'x' + str(alto).zfill(4) + 'x' + \
                      str(espesorg).zfill(3) + 'mm'
        else:
            a = int(ancho) + (2 * int(espesorg)) + 1
            b = int(alto) + int(espesorb)
            if alto > ancho:
                res = 'PIEZA EMBALAJE ' + str(b).zfill(4) + 'x' + str(a).zfill(4) + 'x' + \
                      str(espesorg).zfill(3) + 'mm'
            else:
                res = 'PIEZA EMBALAJE ' + str(a).zfill(4) + 'x' + str(b).zfill(4) + 'x' + \
                      str(espesorg).zfill(3) + 'mm'
        return res

    # Tapa
    @staticmethod
    def get_major_code_type_one(largo, ancho, espesorg):
        if largo > ancho:
            res = str(largo).zfill(4) + str(ancho).zfill(4) + str(espesorg).zfill(3)
        else:
            res = str(ancho).zfill(4) + str(largo).zfill(4) + str(espesorg).zfill(3)
        return res

    # Base
    @staticmethod
    def get_major_code_type_two(largo, ancho, espesorb):
        if largo > ancho:
            res = str(largo).zfill(4) + str(ancho).zfill(4) + str(espesorb).zfill(3)
        else:
            res = str(ancho).zfill(4) + str(largo).zfill(4) + str(espesorb).zfill(3)
        return res

    # Lateral largo
    @staticmethod    
    def get_major_code_type_three(largo, alto, espesorg, alto_tacos, espesorb, distancia_suelo, tipo_palet):
        res = ''
        if tipo_palet == '1':
            a = int(largo) + (2 * int(espesorg)) + 1
            b = int(alto) + int(alto_tacos) - int(distancia_suelo)
            if largo > alto:
                res = str(a).zfill(4) + str(b).zfill(4) + str(espesorg).zfill(3)
            else:
                res = str(b).zfill(4) + str(a).zfill(4) + str(espesorg).zfill(3)
        elif tipo_palet == '0':
            a = int(largo) + (2 * int(espesorg)) + 1
            b = int(alto) + int(alto_tacos) - int(alto_tacos)
            if largo > alto:
                res = str(a).zfill(4) + str(b).zfill(4) + str(espesorg).zfill(3)
            else:
                res = str(b).zfill(4) + str(a).zfill(4) + str(espesorg).zfill(3)
        elif tipo_palet == '4' or tipo_palet == '5':
            a = int(largo) + (2 * int(espesorg)) + 1
            b = int(alto) + int(espesorb)
            if largo > alto:
                res = str(a).zfill(4) + str(b).zfill(4) + str(espesorg).zfill(3)
            else:
                res = str(b).zfill(4) + str(a).zfill(4) + str(espesorg).zfill(3)
        return res

    # TapaLateral corto
    @staticmethod
    def get_major_code_type_four(alto, ancho, espesorg, tipo_palet, espesorb, alto_tacos):
        if tipo_palet != '4' and tipo_palet != '5':
            if alto > ancho:
                res = str(alto).zfill(4) + str(ancho).zfill(4) + str(espesorg).zfill(3)
            else:
                res = str(ancho).zfill(4) + str(alto).zfill(4) + str(espesorg).zfill(3)
        else:
            a = int(ancho) + (2 * int(espesorg)) + 1
            b = int(alto) + int(espesorb)
            if alto > ancho:
                res = str(b).zfill(4) + str(a).zfill(4) + str(espesorg).zfill(3)
            else:
                res = str(a).zfill(4) + str(b).zfill(4) + str(espesorg).zfill(3)
        return res
