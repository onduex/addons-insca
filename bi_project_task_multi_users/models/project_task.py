# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ProjectTask(models.Model):
    _inherit = 'project.task'

    user_ids = fields.Many2many('res.users', relation='project_task_user_rel',
                                column1='task_id', column2='user_id', store=True)
