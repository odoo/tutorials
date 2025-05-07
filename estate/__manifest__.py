# -*- coding: utf-8 -*-
{
    'name': "Real Estate Management (Odoo 18)",
    'version': '18.0.1.0.0',
    'summary': "Manage real estate properties for Odoo 18.",
    'description': """
Module for managing real estate properties, types, tags, and offers,
specifically for Odoo 18.
    """,
    'author': "Kashish Singh",
    'website': "https://www.google.com",
    'category': 'Sales/Real Estate',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ],
    'demo': [
        # 'demo/estate_property_demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'icon': '/estate/static/description/icon.png',
}
