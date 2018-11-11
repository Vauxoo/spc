# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'SPC Sale Costs',
    'summary': 'Costs for SPC Sales',
    'version': '8.0.1.0',
    'category': 'Sales Management',
    'website': 'http://clearcorp.cr',
    'author': 'ClearCorp',
    'license': 'AGPL-3',
    'sequence': 20,
    'application': False,
    'installable': False,
    'auto_install': False,
    'depends': [
        'sale_stock',
        'stock_account_move_line',
    ],
    'data': [
        'security/spc_sale_costs_security.xml',
        'views/picking_type_view.xml',
        'views/account_view.xml',
        'views/sale_order_view.xml',
    ],
}
