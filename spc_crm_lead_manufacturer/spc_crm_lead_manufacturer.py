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
from openerp.tools.translate import _
import math


class CRMLead(models.Model):
    _inherit = 'crm.lead'

    projection = fields.Selection([
        ('sold', 'Sold'), ('committed', 'Commited'), ('expected', 'Expected'),
        ('none', 'None')], string='Projection', default='none')
    principal_address = fields.Selection([
        ('cibersecurity', 'CyberSecurity'), ('datacenter', 'DataCenter'),
        ('it_services', 'IT Services'), ('networking', 'Networking')],
        string='Principal Address')
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
        if self.manufacturer_line_ids:
            if math.fabs(100.0 - estimate_total) != 0.0:
                raise ValidationError(
                    _('Estimate total must be equal to 100%'))

    @api.one
    @api.constrains('projection')
    def _check_projection(self):
        model_data_obj = self.pool.get('ir.model.data')
        _id, _res_model, res_id = model_data_obj.xmlid_lookup(
            self._cr, self._uid, 'crm.stage_lead6')
        if (self.projection == 'sold'):
            if not (self.stage_id.id == res_id):
                raise ValidationError(
                    _('Projection can\'t be Sold when the '
                      'opportunity isn\'t Won'))


class CRMManufacturerLine(models.Model):
    _name = 'spc.crm.lead.manufacturer.line'

    @api.multi
    @api.depends('lead_id.x_planned_cost_product', 'estimate')
    def _compute_total(self):
        for line in self:
            line.total = line.lead_id.x_planned_cost_product * \
                line.estimate/100
        return True

    lead_id = fields.Many2one('crm.lead', string='Lead')
    product_brand_id = fields.Many2one('product.brand', string='Manufacturer')
    code = fields.Char('Code')
    estimate = fields.Float(string='Estimate %')
    total = fields.Float(string="Total", compute='_compute_total')


class ProductBrand(models.Model):
    _inherit = 'product.brand'

    manufacturer_line_ids = fields.One2many(
        'spc.crm.lead.manufacturer.line', 'product_brand_id',
        string='Manufacturer')
