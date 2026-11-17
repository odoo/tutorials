# -*- coding: utf-8 -*-

{
    'name': 'Estate',
    'summary': 'Real estate module',
    'depends': [
        'base'
    ],
    'installable': True,
    'application': True,
    'data': [
        'security/ir.access.csv',

        'views/estate_property_views.xml',
        'views/estate_menu_views.xml',
    ],
}
