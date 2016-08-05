from openerp import models, fields, api


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    @api.depends("order_line")
    def _compute_wk_order_line(self):
        for order in self:
            order.wk_order_line = self.env["sale.order.line"].search([("order_id", '=', order.id), ("wk_under_warranty", '=', True)])
        return True


    # New field for welcome kits
    wk_long_service_level = fields.Char('Service Level Link')
    wk_order_line = fields.One2many("sale.order.line", string="Welcome-Kit Lines", compute="_compute_wk_order_line")

