# -*- coding: utf-8 -*-
{
    'name': "Real Estate",

    'summary': """
        Starting module for "Master the Odoo web framework, chapter 1: Build a new application"
    """,

    'description': """
        Starting module for "Master the Odoo web framework, chapter 1: Build a new application"
    """,

    'author': "Odoo",
    'website': "https://www.odoo.com/",
    'category': 'Tutorials',
    'version': '0.1',
    'application': True,
    'installable': True,
    'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',
        'views/state_property_views.xml',
        'views/estate_menus.xml'
    ],

    'assets': {},
    'license': 'AGPL-3'
}
