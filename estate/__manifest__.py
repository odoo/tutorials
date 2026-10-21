# -*- coding: utf-8 -*-
{
    'name': "Real Estate",

    'summary': """
        Real Estate module for "Server framework 101, chapter 2: A New Application"
    """,

    'description': """
        Real Estate module for "Server framework 101, chapter 2: A New Application"
    """,

    'author': "Dimitris Mystriotis",
    'website': "https://www.odoo.com/",
    'category': 'Tutorials',
    'version': '0.1',
    'application': True,
    'installable': True,
    'depends': ['base'],

    'data': [
        'security/ir.access.csv',

        'views/test_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/res_users_views.xml',
        'views/estate_menus.xml',

    ],
    'assets': {

    },
    'license': 'AGPL-3'
}
