# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'estate',
    'version': '1.0',
    'summary': 'Added Real estate module',
    'description': """
        Real Estate Management Module
        =============================
        Manage properties, offers, and real estate transactions.
    """,
    'depends': [
        'base_setup',
    ],
    'author': 'Muhammad Qasim Shabbir',
    'license': 'LGPL-3',
    'category': 'Real Estate/Brokerage',

    # Required for Odoo 18
    'installable': True,
    'application': True,
    'auto_install': False,

    # Add these later as you create files
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',

        # 1. FIRST: property views (defines actions)
        'views/estate_property_views.xml',
        'data/property_type_data.xml',

        # 2. SECOND: type + tag views (define actions used by menu)
        'views/estate_property_type.xml',
        'views/estate_property_tag_views.xml',

        # 3. LAST: menus (depends on actions above)
        'views/estate_menus.xml',
    ],
    'demo': [
        'demo/property_offer_demo.xml',

    ]
}


