# -*- coding: utf-8 -*-
{
    'name': "Estate",
    'version': '0.1',
    'application': True,
    'installable': True,
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',  
    ],
    'license': 'LGPL-3',
}