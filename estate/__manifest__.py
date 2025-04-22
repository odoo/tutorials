# -*- coding: utf-8 -*-
{
    'name': "Real Estate",
    'summary': """
        Real Estate Tutorial Project
    """,
    'description': """
        Real Estate Tutorial Project
    """,
    'author': "Odoo",
    'website': "https://www.odoo.com/",
    'category': 'Tutorials/Real Estate',
    'version': '18.0.1.1.0',
    'application': True,
    'installable': True,
    'depends': ['base'],
    'data': [
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_menus.xml",
    ],
    'assets': {
    },
    'license': 'AGPL-3'
}
