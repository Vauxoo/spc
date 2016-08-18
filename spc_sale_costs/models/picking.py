# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    @api.multi
    @api.depends('picking_type_id', 'picking_type_id.cost_on_sale_order',
                 'group_id')
    def _compute_cost_sale_order_id(self):
        for picking in self:
            if picking.picking_type_id.cost_on_sale_order:
                picking.cost_sale_order_id = self.env['sale.order'].search(
                    [('procurement_group_id', '=', picking.group_id.id),
                     ('company_id', '=', picking.company_id.id)],
                    limit=1)
            else:
                picking.cost_sale_order_id = False

    cost_sale_order_id = fields.Many2one(
        'sale.order', string='Cost Sale Order',
        compute='_compute_cost_sale_order_id', store=True)
