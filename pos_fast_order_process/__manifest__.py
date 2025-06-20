# Part of Odoo. See LICENSE file for full copyright and licensing details.s.
{
    "name": "Fast Order Process POS",
    "version": "18.0.1.0.0",
    "license": "LGPL-3",
    "author": "Odoo PS",
    "category": "Point of Sale",
    "website": "https://www.odoo.com",
    "depends": ["point_of_sale", "pos_loyalty", "pos_restaurant"],
    "summary": "Fast Order Process POS",
    "description": """
        - Your Fast Order Process is here.
    """,
    "data": [
        "views/res_config_settings_views.xml",
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "pos_fast_order_process/static/src/**/*",
        ],
    },
    "installable": True,
}
