# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "rsbh",
    'category': 'Real Estate',
    'license': 'LGPL-3',
    'description': "A module for managing real estate properties",
    'depends':['base'],
    'data': [
        "security/ir.model.access.csv",
        "views/estate_property_offer_view.xml",
        "views/estate_property_type_view.xml",
        "views/estate_property_tag_view.xml",
        "views/estate_property_view.xml",
        "views/inherited_user_view.xml",
        "views/estate_menus.xml"
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
