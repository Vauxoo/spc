# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Addons modules by CLEARCORP S.A.
#    Copyright (C) 2009-TODAY CLEARCORP S.A. (<http://clearcorp.co.cr>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api
from openerp.exceptions import ValidationError
import math


class CRMLead(models.Model):
    _inherit = 'crm.lead'

    projection = fields.Selection([
        ('sold', 'Sold'), ('committed', 'Commited'), ('expected', 'Expected'),
        ('none', 'None')], string='Projection', default='sold')
    principal_address = fields.Selection([
        ('cibersecurity', 'CyberSecurity'), ('datacenter', 'DataCenter'),
        ('it_services', 'IT Services'), ('networking', 'Networking')],
        string='Principal Address', default='cibersecurity')
    manufacturer_line_ids = fields.One2many(
        'spc.crm.lead.manufacturer.line', 'lead_id', string='Manufacturer')

    @api.one
    @api.constrains('manufacturer_line_ids')
    def _check_manufacturer_line_ids(self):
        estimate_total = 0
        total = 0
        for line in self.manufacturer_line_ids:
            estimate_total += line.estimate
            total += line.total
        if math.fabs(self.x_planned_cost_product - total) > 100:
            raise ValidationError("Total must be equal to product cost (" +
                                  str(self.x_planned_cost_product) + ")")
        if math.fabs(100 - estimate_total) > 10:
            raise ValidationError("Estimate total must be equal to 100%")


class CRMManufacturerLine(models.Model):
    _name = 'spc.crm.lead.manufacturer.line'

    @api.multi
    @api.depends('lead_id.x_planned_cost_product')
    def _compute_total(self):
        for line in self:
            line.total = line.lead_id.x_planned_cost_product * \
                line.estimate/100
        return True

    lead_id = fields.Many2one('crm.lead', string='Lead')
    product_brand_id = fields.Many2one('product.brand', string='Manufacturer')
    code = fields.Char('Code')
    estimate = fields.Float(string='Estimate')
    total = fields.Float(string="Total", compute='_compute_total')


class ProductBrand(models.Model):
    _inherit = 'product.brand'

    manufacturer_line_ids = fields.One2many(
        'spc.crm.lead.manufacturer.line', 'product_brand_id',
        string='Manufacturer')
