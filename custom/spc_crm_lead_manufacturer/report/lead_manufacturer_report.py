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

from openerp import models
from openerp.report import report_sxw
from openerp.tools import SUPERUSER_ID


class LeadManufacturerReport(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(LeadManufacturerReport, self).__init__(
            cr, uid, name, context=context)
        self.localcontext.update({
            'get_leads': self._get_leads,
            'get_user': self._get_user,
        })

    def _get_user(self, user_id):
        return self.pool.get('res.users').browse(
            self.cr, self.uid, [user_id], context=self.localcontext)

    def _get_leads(self, lead_ids):
        leads = self.pool.get('crm.lead').browse(
            self.cr, SUPERUSER_ID, lead_ids, context=self.localcontext)
        lead_item = leads[0]
        return leads


class report_lead_manufacturer_xls(models.AbstractModel):
    _name = 'report.spc_crm_lead_manufacturer.report_lead_manufacturer'
    _inherit = 'report.abstract_report'
    _template = 'spc_crm_lead_manufacturer.report_lead_manufacturer'
    _wrapped_report_class = LeadManufacturerReport
