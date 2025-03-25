{
    "name": "salesperson_button_pos",
    "version": "1.0",
    "author": "assh-odoo",
    "depends": ["point_of_sale", "hr"],
    "data": ["views/pos_order_view.xml"],
    "assets": {
        "point_of_sale._assets_pos": [
            "salesperson_button_pos/static/src/**/*",
        ],
    },
    "installable": True,
    "license": "LGPL-3",
}
