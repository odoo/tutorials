# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "POS Salesperson",
    "version": "1.0",
    "author": "Ayush",
    "summary": "Allows to select a salesperson for POS order",
    "category": "Tutorials/POS Salesperson",
    "depends": ["point_of_sale", "hr"],
    "data": [
        "views/pos_order_views.xml"
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "pos_salesperson/static/src/**/*"
        ]
    },
    "installable": True,
    "license": "LGPL-3"
}
