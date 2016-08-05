# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class SaleOrderLine(models.Model):

    _inherit = 'sale.order.line'

    # New fields for welcome kits
    wk_contract = fields.Char('Contract')
    wk_service_level = fields.Char('Service Level')
    wk_site_name = fields.Char('Site Name')
    wk_product_number = fields.Char('Product Number')
    wk_serial_number = fields.Char('Equipment Serial Number')
    wk_under_warranty = fields.Boolean('Print in Welcome Kit')
    wk_begin_date = fields.Date('Begin Date')
    wk_end_date = fields.Date('End Date')

