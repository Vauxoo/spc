# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import re
import httplib2
import logging
from apiclient import discovery
from oauth2client.client import Credentials
from openerp import models, fields, api, _
from openerp.exceptions import Warning

SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_ID = '149905831071-d08bancbk563mj8avccqnfpc12rllimv.apps.googleusercontent.com'
CLIENT_SECRET = '8KXLgti93Qn990cnspaZ_0Cp'
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

_logger = logging.getLogger(__name__)

class Lead(models.Model):

    _inherit = 'crm.lead'
    _order = 'id ASC'

    @api.one
    def get_credentials(self):
        ir_config = self.env['ir.config_parameter']
        credentials_json = ir_config.sudo().get_param(
            'spc_crm_bc_credentials')
        if credentials_json:
            credentials = Credentials.new_from_json(credentials_json)
        else:
            credentials = None
        if not credentials or credentials.invalid:
            raise Warning(_(
                'Google Drive is not yet configured. Please contact'
                'your administrator.'))
        return credentials

    @api.one
    def set_credentials(self, credentials):
        ir_config = self.env['ir.config_parameter']
        if credentials:
            ir_config.sudo().set_param(
                'spc_crm_bc_credentials', credentials.to_json(),
                groups=['base.group_system'])
            _logger.info('Storing new credentials')
            return True
        return False

    @api.one
    def read_data_from_business_case(self, attachment):
        credentials = self.get_credentials()[0]
        store_credentials = False
        if credentials. access_token_expired:
            store_credentials = True
        http = credentials.authorize(httplib2.Http())
        discoveryUrl = (
            'https://sheets.googleapis.com/$discovery/rest?version=v4')
        service = discovery.build(
            'sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)

        regex = re.compile('\/d\/(.*)\/')
        res = regex.search(attachment.url)
        # spreadsheetId = '1NoBIVGluLnhX3SMZkeFjReQMKrdItnb6VsN28kXryz8'
        spreadsheetId = res.group(1)
        rangeName = 'Resultados!C8:D13'
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheetId, range=rangeName).execute()
        values = result.get('values', [])
        if store_credentials:
            self.set_credentials(credentials)
        return {
            'x_planned_cost_product': float(values[0][0]),
            'x_planned_margin_product': float(values[0][1]),
            'x_planned_cost_services_eng': float(values[1][0]),
            'x_planned_margin_services_eng': float(values[1][1]),
            'x_planned_cost_services_adm': float(values[2][0]),
            'x_planned_margin_services_adm': float(values[2][1]),
            'x_unexpected_cost': float(values[3][0]),
            'x_unexpected_margin': float(values[3][1]),
            'planned_cost': float(values[5][0]),
            'x_planned_margin': float(values[5][1]),
        }

    @api.multi
    def sync_business_case(self):
        for lead in self:
            # Verify if this lead has an attachment
            config_param = self.env['ir.config_parameter']
            tempate_str = config_param.get_param('spc_crm_bc_template')
            config_id = tempate_str and int(tempate_str) or False
            if not config_id:
                raise Warning(_(
                    'The sync template is not configured. Please ask the'
                    ' Administrator to set it up.'))
            config = self.env['google.drive.config'].sudo().browse(config_id)
            model = config.model_id
            filter_name = config.filter_id and config.filter_id.name or False
            record = self.read([])[0]
            record.update({'model': model.name, 'filter': filter_name})
            name_gdocs = config.name_template
            try:
                name_gdocs = name_gdocs % record
            except:
                raise Warning(_(
                    'At least one key cannot be found in your Google Drive'
                    ' name pattern'))
            attachment = self.env['ir.attachment'].search([
                ('res_model', '=', model.model),
                ('name', '=', name_gdocs),
                ('res_id', '=', lead.id)], limit=1)
            if attachment:
                data = lead.read_data_from_business_case(attachment)[0]
                lead.write(data)
        return True

    def _get_selection_values(self):
        companies = self.env.user.company_ids
        return [(company.id, company.name) for company in companies]

    @api.depends('company_id')
    def _compute_change_company_id(self):
        for lead in self:
            lead.change_company_id = False

    def _inverse_change_company_id(self):
        for lead in self:
            lead.company_id = lead.change_company_id

    change_company_id = fields.Selection(
        selection=_get_selection_values,
        string='Change Company', compute='_compute_change_company_id',
        inverse='_inverse_change_company_id',
        help='Use this field to change this opportunity between companies.')
    ref_sale_ids = fields.One2many(
        'sale.order', 'ref_oportunity_id', string='Sale Orders', readonly=True)
