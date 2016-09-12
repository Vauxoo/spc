# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api


class StockMove(models.Model):

    _inherit = 'stock.move'

    @api.model
    def create(self, vals):
        res = super(StockMove, self).create(vals)
        if 'group_id' in vals and 'picking_id' in vals:
            picking = self.env['stock.picking'].search(
                [('id', '=', vals['picking_id'])])
            picking.get_cost_sale_order()
        return res

    @api.multi
    def write(self, vals):
        res = super(StockMove, self).write(vals)
        if 'group_id' in vals or 'picking_id' in vals:
            picking_obj = self.env['stock.picking']
            for move in self:
                picking_id = 'picking_id' in vals and \
                    vals['picking_id'] or move.picking_id.id
                picking = picking_obj.search(
                    [('id', '=', picking_id)])
                picking.get_cost_sale_order()
        return res
