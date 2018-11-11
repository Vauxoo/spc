# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from oauth2client.client import OAuth2WebServerFlow
from openerp import models, fields, api

SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_ID = '149905831071-d08bancbk563mj8avccqnfpc12rllimv.apps.googleusercontent.com'
CLIENT_SECRET = '8KXLgti93Qn990cnspaZ_0Cp'
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

class SaleConfiguration(models.TransientModel):

    _inherit = 'sale.config.settings'

    @api.depends('spc_crm_bc_authorization_code')
    def _compute_spc_crm_bc_uri(self):
        flow = OAuth2WebServerFlow(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            scope=SCOPES,
            redirect_uri=REDIRECT_URI)
        auth_uri = flow.step1_get_authorize_url()
        for config in self:
            config.spc_crm_bc_uri = auth_uri

    spc_crm_bc_template = fields.Many2one(
        'google.drive.config', string='BC Template')
    spc_crm_bc_authorization_code = fields.Char(
        'BC Sync Authorization Code')
    spc_crm_bc_uri = fields.Char(
        'BC Sync URI', compute='_compute_spc_crm_bc_uri')

    @api.multi
    def get_default_spc_crm_bc_template(self):
        config_param = self.env['ir.config_parameter']
        tempate_str = config_param.get_param('spc_crm_bc_template')
        tempate_id = tempate_str and int(tempate_str) or False
        return {
            'spc_crm_bc_template': tempate_id
        }

    @api.one
    def set_spc_crm_bc_template(self):
        config_param = self.env['ir.config_parameter']
        if self.spc_crm_bc_template:
            config_param.set_param(
                'spc_crm_bc_template', str(self.spc_crm_bc_template.id),
                groups=['base.group_system'])
        return True

    @api.multi
    def get_default_spc_crm_bc_authorization_code(self):
        config_param = self.env['ir.config_parameter']
        return {
            'spc_crm_bc_authorization_code': config_param.get_param(
                'spc_crm_bc_authorization_code')
        }

    @api.one
    def set_spc_crm_bc_authorization_code(self):
        config_param = self.env['ir.config_parameter']
        auth_code = self.spc_crm_bc_authorization_code
        if auth_code and auth_code != config_param.get_param(
                'spc_crm_bc_authorization_code'):
            config_param.set_param(
                'spc_crm_bc_authorization_code', auth_code,
                groups=['base.group_system'])
            flow = OAuth2WebServerFlow(
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                scope=SCOPES,
                redirect_uri=REDIRECT_URI)
            credentials = flow.step2_exchange(auth_code)
            config_param.set_param(
                'spc_crm_bc_credentials', credentials.to_json(),
                groups=['base.group_system'])
        return True
