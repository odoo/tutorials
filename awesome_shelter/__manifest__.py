# -*- coding: utf-8 -*-
{
    "name": "Awesome Shelter",
    "summary": """
        Companion addon for the Odoo JS Framework Training
    """,
    "description": """
        Companion addon for the Odoo JS Framework Training
    """,
    "author": "Odoo",
    "website": "https://www.odoo.com/",
    "category": "Tutorials",
    "version": "0.1",
    "application": True,
    "installable": True,
    "depends": ["base", "web", "contacts"],
    "data": [
        "views/views.xml",
        "security/ir.model.access.csv",
        "data/shelter_data.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "awesome_shelter/static/src/**/*",
        ],
    },
    "license": "AGPL-3",
}
