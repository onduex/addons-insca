# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ReportProjectTaskUser(models.Model):
    _inherit = "report.project.task.user"

    user_ids = fields.Many2many('res.users', relation='project_task_user_rel',
                                column1='task_id', column2='user_id', store=True)

    def _select(self):
        return super(ReportProjectTaskUser, self)._select() + ", t.task_id as task_id"

    def _group_by(self):
        return super(ReportProjectTaskUser, self)._group_by() + ", t.user_id"
