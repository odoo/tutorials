# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Real Estate",
    'version': '1.0',
    'author': "rsbh",
    'category': 'Real Estate/Brokerage',
    'license': 'LGPL-3',
    'description': "A module for managing real estate properties",
    'depends':['base',"website"],
    'data': [
        'report/estate_property_templates.xml',
        'report/estate_property_reports.xml',
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/estate_property_offer_view.xml",
        "views/estate_property_type_view.xml",
        "views/estate_property_tag_view.xml",
        "views/estate_property_view.xml",
        "views/inherited_user_view.xml",
        "views/estate_menus.xml",
        "data/estate_data.xml"
    ],
    'demo': [
         "demo/estate_property_demo.xml",
         "demo/estate_property_offer_demo.xml"
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
