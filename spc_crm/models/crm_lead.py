# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class Lead(models.Model):

    _inherit = 'crm.lead'
    _order = 'id ASC'

    def _get_selection_values(self):
        companies = self.env.user.company_ids
        return [(company.id, company.name) for company in companies]

    @api.depends('company_id')
    def _compute_change_company_id(self):
        for lead in self:
            lead.change_company_id = False

    def _inverse_change_company_id(self):
        for lead in self:
            lead.company_id = lead.change_company_id

    change_company_id = fields.Selection(
        selection=_get_selection_values,
        string='Change Company', compute='_compute_change_company_id',
        inverse='_inverse_change_company_id',
        help='Use this field to change this opportunity between companies.')
