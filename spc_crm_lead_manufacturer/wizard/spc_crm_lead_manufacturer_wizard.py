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
from openerp import models, fields


class CRMManufacturerLineWizard(models.TransientModel):
    _name = 'spc.crm.lead.manufacturer.wizard'

    user_ids = fields.Many2many(
        'res.users', string='Salesperson')
    company_ids = fields.Many2many(
        'res.company', string='Company', required=True)

    def print_report(self, cr, uid, ids, context=None):
        """#line_obj = self.pool.get('account.analytic.line')
        data = {}
        data['form'] = self.read(cr, uid , ids, context=context)[0]
        ids_chk = line_obj.search(cr, uid, [
                ('date', '>=', data['form']['date_from']),
                ('date', '<=', data['form']['date_to']),
                ('journal_id', 'in', data['form']['journal_ids']),
                ('user_id', 'in', data['form']['employee_ids']),
                ], context=context)
        if not ids_chk:
            raise osv.except_osv(_('Insufficient Data!'), _('No record(s) found for this report.'))

        data['form']['journal_ids'] = [(6, 0, data['form']['journal_ids'])] # Improve me => Change the rml/sxw so that it can support withou [0][2]
        data['form']['employee_ids'] = [(6, 0, data['form']['employee_ids'])]
        datas = {
            'ids': [], # LEADS
            'model': 'account.analytic.line',# crm.lead
            'form': data['form']
        }"""
        datas = {}
        return self.pool['report'].get_action(
            cr, uid, [], 'spc_crm_lead_manufacturer.report_lead_manufacturer', data=datas, context=context
        )
