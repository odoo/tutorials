# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Estate',
    'summary': """
        Starting module for "Server framework 101, chapter 2: Build an estate app"
    """,

    'description': """
        Starting module for "Server framework 101, chapter 2: Build an estate app"
    """,

    'author': "Odoo",
    'website': "https://www.odoo.com/",
    'category': 'Tutorials/Estate',
    'version': '0.1',
    'application': True,
    'installable': True,
    'depends': ['base', 'web'],

    'data': [
            'security/ir.model.access.csv',
            'views/estate_property_views.xml',
            'views/estate_menu_views.xml'
            ],

    'license': 'AGPL-3'
}
