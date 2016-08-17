# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    @api.multi
    @api.depends('picking_ids.picking_type_id.cost_on_sale_order',
                 'picking_ids.state')
    def _compute_cost_picking_ids(self):
        for order in self:
            picking_ids = []
            for picking in order.picking_ids:
                if picking.picking_type_id.cost_on_sale_order:
                    picking_ids.append(picking.id)
            order.cost_picking_ids = self.env['stock.picking'].search(
                [('id', 'in', picking_ids),
                 ('company_id', '=', order.company_id.id)])

    @api.multi
    @api.depends(
        'invoice_ids.move_id.line_id.credit', 'cost_picking_ids')
    def _compute_cost_and_income(self):
        for order in self:
            # Get income lines
            move_ids = []
            for invoice in order.invoice_ids:
                move_ids.append(invoice.move_id.id)
            order.income_line_ids = self.env['account.move.line'].search(
                [('move_id', 'in', move_ids), ('credit', '>', 0.0)])
            # Get cost lines
            move_ids = []
            for picking in order.cost_picking_ids:
                ids = self.env['account.move'].search(
                    [('ref', '=', picking.name),
                     ('company_id', '=', order.company_id.id)])._ids
                if ids:
                    move_ids += list(ids)
            order.cost_line_ids = self.env['account.move.line'].sudo().search(
                [('move_id', 'in', move_ids), ('debit', '>', 0.0)])

    @api.multi
    @api.depends('income_line_ids', 'cost_line_ids', 'cost_picking_ids')
    def _compute_cost_error(self):
        for order in self:
            if not order.income_line_ids and not order.cost_line_ids:
                order.cost_error = 'nd'
            elif order.income_line_ids and order.cost_line_ids:
                flag = True
                for picking in order.cost_picking_ids:
                    if picking.state not in ['cancel', 'done']:
                        flag = False
                        break
                order.cost_error = flag and 'ok' or 'error'
            elif not order.income_line_ids and order.cost_line_ids:
                order.cost_error = 'error'
            elif order.income_line_ids and not order.cost_line_ids:
                order.cost_error = order.cost_picking_ids and 'error' or 'ok'
            else:
                order.cost_error = 'error'

    @api.multi
    @api.depends('income_line_ids.credit', 'cost_line_ids.debit',)
    def _compute_period_error(self):
        for order in self:
            if not order.cost_line_ids:
                order.period_error = 'ok'
            else:
                state = 'ok'
                # Get the oldest income line
                income_line = self.env['account.move.line'].search(
                    [('id', 'in', order.income_line_ids._ids)],
                    order='date asc', limit=1)
                if income_line:
                    for line in order.cost_line_ids:
                        if line.period_id.id != income_line.period_id.id:
                            state = 'error'
                            break
                order.period_error = state

    @api.multi
    @api.depends('income_line_ids.credit', 'cost_line_ids.debit')
    def _compute_profit_percentage(self):
        for order in self:
            total_credit = 0.0
            total_debit = 0.0
            for line in order.income_line_ids:
                total_credit += line.credit
            for line in order.cost_line_ids:
                total_debit += line.debit
            try:
                order.profit_percentage = (
                    total_credit - total_debit) / total_credit
            except ZeroDivisionError:
                order.profit_percentage = 0.0

    cost_picking_ids = fields.One2many(
        'stock.picking', string='Cost Pickings',
        compute='_compute_cost_picking_ids')
    income_line_ids = fields.One2many(
        'account.move.line', string='Income Lines',
        compute='_compute_cost_and_income')
    cost_line_ids = fields.One2many(
        'account.move.line', string='Cost Lines',
        compute='_compute_cost_and_income')
    cost_error = fields.Selection(
        [('nd', 'N/D'), ('ok', 'OK'), ('error', 'Error')], string='Cost Error',
        compute='_compute_cost_error', default='ok', store=True)
    period_error = fields.Selection(
        [('ok', 'OK'), ('error', 'Error')], string='Period Error',
        compute='_compute_period_error', default='ok', store=True)
    profit_percentage = fields.Float(
        'Profit Percentage', digits=dp.get_precision('Account'),
        compute='_compute_profit_percentage', default=0.0, store=True)
