# -*- coding: utf-8 -*-

{
    "name": "Real Estate",
    "version": "0.1",
    "category": "Administration",
    "sequence": 100,
    "license": "LGPL-3",
    "author": "alup",
    "summary": "Track real estate",
    "description": "",
    "website": "https://www.odoo.com/page/estate",
    "depends": [
        "base_setup",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_menus.xml",
    ],
    "demo": [],
    "css": [],
    "installable": True,
    "application": True,
    "auto_install": False,
}
