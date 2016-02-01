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


class CRMManufacturerLineWizard(models.TransientModel):
    _name = 'spc.crm.lead.manufacturer.wizard'

    user_ids = fields.Many2many(
        'res.users', string='Salesperson')
    company_ids = fields.Many2many(
        'res.company', string='Company', required=True)
    date_from = fields.Date('Start Date', required=True)
    date_to = fields.Date('End Date', required=True)

    @api.multi
    def print_report(self):
        datas = {}
        if not self.env['res.users'].has_group('base.group_sale_manager'):
            self.user_ids = [self._uid]
            datas['user_id'] = self._uid
        leads = []
        query_date = """SELECT EXTRACT(YEAR FROM date_deadline) as year,
            EXTRACT(MONTH FROM date_deadline) as month
            FROM crm_lead
            WHERE date_deadline >= %s
            AND date_deadline <= %s
            AND company_id IN %s"""
        if self.user_ids._ids:
            query_date += """AND user_id IN %s
            GROUP BY year, month
            ORDER BY year, month ASC;"""
            self._cr.execute(
                query_date, (
                    self.date_from, self.date_to,
                    tuple(self.company_ids._ids),
                    tuple(self.user_ids._ids)))
        else:
            query_date += """GROUP BY year, month
            ORDER BY year, month ASC;"""
            self._cr.execute(
                query_date, (
                    self.date_from, self.date_to,
                    tuple(self.company_ids._ids),))
        dates = self._cr.fetchall()
        for year, month in dates:
            query = """SELECT id, user_id
            FROM crm_lead
            WHERE date_deadline >= %s
            AND date_deadline <= %s
            AND company_id IN %s"""
            if self.user_ids._ids:
                query += """AND user_id IN %s
                AND EXTRACT(YEAR FROM date_deadline) = %s
                AND EXTRACT(MONTH FROM date_deadline) = %s
                ORDER BY date_deadline;"""
                self._cr.execute(
                    query, (
                        self.date_from, self.date_to,
                        tuple(self.company_ids._ids),
                        tuple(self.user_ids._ids),
                        year, month))
            else:
                query += """AND EXTRACT(YEAR FROM date_deadline) = %s
                AND EXTRACT(MONTH FROM date_deadline) = %s
                ORDER BY date_deadline;"""
                self._cr.execute(
                    query, (
                        self.date_from, self.date_to,
                        tuple(self.company_ids._ids),
                        year, month))
            leads.append((
                year, month, [item[0] for item in self._cr.fetchall()],))
        datas['leads'] = leads
        return self.pool['report'].get_action(
            self._cr, self._uid, [],
            'spc_crm_lead_manufacturer.report_lead_manufacturer',
            data=datas, context=self._context
        )
