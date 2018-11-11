# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import models, fields


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    ref_oportunity_id = fields.Many2one(
        'crm.lead', string='Opportunity', readonly=True)