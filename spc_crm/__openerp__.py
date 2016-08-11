# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'SPC Custom CRM',
    'summary': 'Custom extensions for SPC CRM',
    'version': '8.0.1.0',
    'category': 'Customer Relationship Management',
    'website': 'http://clearcorp.cr',
    'author': 'ClearCorp',
    'license': 'AGPL-3',
    'sequence': 3,
    'application': False,
    'installable': True,
    'auto_install': False,
    'depends': [
        'crm',
        'sale_crm',
    ],
    'data': [
        'views/crm_lead_view.xml',
        'views/sale_order_view.xml',
        'views/sale_config_settings_view.xml',
    ]
}
