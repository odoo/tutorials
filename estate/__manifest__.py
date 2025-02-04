# -*- coding: utf-8 -*-
{
    'name': "Real Estate Module",
    'summary': "This is the real estate module that is used for buying and selling propertise!!",
    'description': "This is the real estate module that is used for buying and selling propertise!!",
    'version': '0.1',
    'application': True,
    'category': 'Tutorials',
    'installable': True,
    'depends': ['base'],
    'data': [
        "views/estate_property_views.xml",
        "views/estate_menus.xml",
        "security/ir.model.access.csv",
    ],
    'assets': {
    },
    'license': 'AGPL-3'
}
