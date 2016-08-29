# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    @api.multi
    def action_reassign_sale_costs(self):
        for order in self:
            # Get the oldest income
            income_line = self.env['account.move.line'].search(
                [('id', 'in', order.income_line_ids._ids)], order='date asc',
                limit=1)
            if income_line:
                for line in order.cost_line_ids:
                    if line.period_id.id != income_line.period_id.id:
                        if line.move_id.state == 'posted':
                            line.move_id.button_cancel()
                            line.write({
                                'period_id': income_line.period_id.id,
                                'date': income_line.date,
                            })
                            line.move_id.button_validate()
                        else:
                            line.write({
                                'period_id': income_line.period_id.id,
                                'date': income_line.date,
                            })

    @api.multi
    @api.depends(
        'invoice_ids', 'invoice_ids.move_id',
        'invoice_ids.move_id.line_id.account_id.income_on_sale_order')
    def _compute_income_line_ids(self):
        for order in self:
            # Get income lines
            move_ids = []
            for invoice in order.invoice_ids:
                move_ids.append(invoice.move_id.id)
            income_move_lines = self.env[
                'account.move.line'].search(
                [('move_id', 'in', move_ids),
                 ('account_id.income_on_sale_order', '=', True)])
            # Set income lines
            order.income_line_ids = income_move_lines

    @api.multi
    @api.depends(
        'cost_picking_ids', 'cost_picking_ids.state', 'invoice_ids',
        'invoice_ids.move_id', 'cost_line_ids',
        'invoice_ids.move_id.line_id.account_id.income_on_sale_order',
        'invoice_ids.move_id.period_id', 'invoice_ids.move_id.date',
        'cost_line_ids.period_id', 'cost_line_ids.date')
    def _compute_sale_error_states(self):
        for order in self:
            # Get cost lines
            pickings_transfered = True
            for picking in order.cost_picking_ids:
                if picking.state not in ['cancel', 'done']:
                    pickings_transfered = False

            income_move_lines = order.income_line_ids
            # Get cost error state
            if not income_move_lines and not order.cost_line_ids:
                state_cost = 'nd'
            elif income_move_lines and order.cost_line_ids:
                state_cost = pickings_transfered and 'ok' or 'error'
            elif not income_move_lines and order.cost_line_ids:
                state_cost = 'error'
            elif income_move_lines and not order.cost_line_ids:
                state_cost = order.cost_picking_ids and 'error' or 'ok'
            else:
                state_cost = 'error'

            # Get period error state
            if not order.cost_line_ids:
                period_state = 'ok'
            else:
                period_state = 'ok'
                # Get the oldest income line
                income_line = self.env['account.move.line'].search(
                    [('id', 'in', income_move_lines._ids)],
                    order='date asc', limit=1)
                if income_line:
                    for line in order.cost_line_ids:
                        if line.period_id.id != income_line.period_id.id:
                            period_state = 'error'
                            break

            # Set cost error state
            order.cost_error = state_cost
            # Set period error state
            order.period_error = period_state

    @api.multi
    @api.depends(
        'cost_line_ids', 'invoice_ids', 'invoice_ids.move_id',
        'invoice_ids.move_id.line_id.account_id.income_on_sale_order')
    def _compute_profit_percentage(self):
        for order in self:
            total_credit = 0.0
            total_debit = 0.0
            for line in order.income_line_ids:
                total_credit += line.credit
            for line in order.cost_line_ids:
                total_debit += line.debit
            try:
                order.profit_percentage = ((
                    total_credit - total_debit) / total_credit) * 100
            except ZeroDivisionError:
                order.profit_percentage = 0.0

    cost_picking_ids = fields.One2many(
        'stock.picking', 'cost_sale_order_id', string='Cost Pickings')
    income_line_ids = fields.One2many(
        'account.move.line', string='Income Lines',
        compute='_compute_income_line_ids')
    cost_line_ids = fields.One2many(
        'account.move.line', 'cost_sale_order_id', string='Cost Lines')
    cost_error = fields.Selection(
        [('nd', 'N/D'), ('ok', 'OK'), ('error', 'Error')],
        string='Cost Error', compute='_compute_sale_error_states',
        store=True)
    period_error = fields.Selection(
        [('ok', 'OK'), ('error', 'Error')], string='Period Error',
        compute='_compute_sale_error_states', store=True)
    profit_percentage = fields.Float(
        'Profit Percentage', digits=dp.get_precision('Account'),
        compute='_compute_profit_percentage', store=True)
