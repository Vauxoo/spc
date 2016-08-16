# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class PickingType(models.Model):

    _inherit = 'stock.picking.type'

    cost_on_sale_order = fields.Boolean('Cost on Sale Orders')
