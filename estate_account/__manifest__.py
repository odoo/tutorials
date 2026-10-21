# -*- coding: utf-8 -*-
{
    'name': "Real Estate Account",

    'summary': """
        Real Estate Account module for "Server framework 101, Chapter 13: Interact With Other Modules"
    """,

    'description': """
        Real Estate Account module for "Server framework 101, Chapter 13: Interact With Other Modules"
    """,

    'author': "Dimitris Mystriotis",
    'website': "https://www.odoo.com/",
    'category': 'Tutorials',
    'version': '0.1',
    'application': True,
    'installable': True,
    'depends': ['base', 'estate', 'account'],

    'data': [
        'security/ir.access.csv',
    ],
    'assets': {

    },
    'license': 'AGPL-3'
}
