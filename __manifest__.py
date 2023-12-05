# -*- coding: utf-8 -*-

{
    'name': 'Sale order approval',
    'version': '1.0.0.3',
    'author':'Soft-integration',
    'category': 'Sale',
    'summary': 'Sale order approval',
    'description': "",
    'depends': [
        'sale'
    ],
    'data': [
        'security/sale_order_approval_security.xml',
        'views/sale_views.xml',
        'views/res_config_settings_views.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
