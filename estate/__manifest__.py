# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Real Estate",
    "version": "1.0",
    "author": "Odoo PS",
    "license": "LGPL-3",
    "website": "https://www.odoo.com/",
    "depends": ["base", "mail"],
    "application": True,
    "category": "Real Estate/Brokerage",
    "description": """
    Real Estate Test Description
    """,
    "data": [
        "data/master_data_estate_property_type.xml",
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/res_users_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_menus.xml",
    ],
    "demo": [
        "demo/demo_property_data.xml",
        "demo/demo_property_offer.xml"
    ]
}
