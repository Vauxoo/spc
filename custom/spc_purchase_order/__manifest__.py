# -*- coding: utf-8 -*-
#    Copyright (C) 2009-TODAY CLEARCORP S.A. (<http://clearcorp.co.cr>).

{
    'name': 'SPC Purchase order',
    'version': '1.1',
    'category': 'Purchase Management',
    'sequence': 10,
    'summary': 'Removes the default value in field picking_type_id, '\
        'adds fields to purchase order line.',
    'author': 'ClearCorp',
    'images': [],
    'depends': ['purchase'],
    'data': [
        'spc_purchase_order.xml',
        'purchase_order_line_view.xml',
        ],
    'test': [],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'AGPL-3',
}
