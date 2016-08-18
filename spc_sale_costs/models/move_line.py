# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class AccountMoveLine(models.Model):

    _inherit = 'account.move.line'

    @api.multi
    @api.depends('stock_picking_id.cost_sale_order_id',
                 'account_id.cost_on_sale_order')
    def _compute_cost_sale_order_id(self):
        for line in self:
            if line.stock_picking_id and \
                    line.stock_picking_id.cost_sale_order_id and \
                    line.account_id.cost_on_sale_order and \
                    line.stock_picking_id.company_id.id == line.company_id.id:
                line.cost_sale_order_id = \
                    line.stock_picking_id.cost_sale_order_id
            else:
                line.cost_sale_order_id = False

    cost_sale_order_id = fields.Many2one(
        'sale.order', string='Cost Sale Order',
        compute='_compute_cost_sale_order_id', store=True)
