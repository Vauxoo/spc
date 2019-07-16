# -*- coding: utf-8 -*-
# © 2018 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'SPC - Sale followers',
    'summary': 'Remove automatic followers from sale orders and leads',
    'version': '1.0',
    'category': 'Customer Relationship Management',
    'author': 'ClearCorp',
    'license': 'AGPL-3',
    'sequence': 3,
    'application': False,
    'installable': True,
    'auto_install': False,
    'depends': [
        'crm',
        'sale',
        'sale_subscription',
    ],
    'data': []
}
