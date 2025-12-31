# -*- coding: utf-8 -*-
{
    'name': "estate",

    'description': """
        A real-estate application"
    """,

    'author': "meet kavathiya",
    'website': "https://www.odoo.com/",
    'category': 'Real-estate',
    'version': '0.1',
    'application': True,
    'installable': True,
    'depends': ['base', 'web'],

    'data': ['security/ir.model.access.csv',
             'views/estate_property_views.xml',
             'views/estate_menus.xml'],
    'assets': {

    },
    'license': 'LGPL-3'
}
