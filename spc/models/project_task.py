# -*- coding: utf-8 -*-
from odoo import api, fields, models

from datetime import datetime


class ProjectTask(models.Model):
    _inherit = 'project.task'

    date_stage_change = fields.Datetime(
        'Fecha de último cambio de etapa',
        readonly=True
    )

    @api.multi
    def write(self, vals):
        if 'stage_id' in vals:
            vals['date_stage_change'] = datetime.now()
        return super(ProjectTask, self).write(vals)
