# -*- coding: utf-8 -*-
{
    'name': 'Real Estate',
    'summary': """
        Real estate"
    """,
    'description': """
        Descrption"
    """,
    'author': 'Antonio',
    'category': 'Tutorials',
    'version': '1.0',
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
