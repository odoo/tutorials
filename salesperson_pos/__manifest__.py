{
    "name": "salesperson_pos" ,
    "version": "1.0",
    "license": "LGPL-3",
    "depends": ["point_of_sale","hr"],
    "data": ["views/pos_order_views.xml", "views/account_move.xml"],
    "assets": {
        "point_of_sale._assets_pos": [
            "salesperson_pos/static/src/models/pos_order.js",
            "salesperson_pos/static/src/control_buttons/control_buttons.js",
            "salesperson_pos/static/src/control_buttons/control_buttons.xml",
            "salesperson_pos/static/src/select_salesperson_button/select_salesperson_button.js",
            "salesperson_pos/static/src/select_salesperson_button/select_salesperson_button.xml",
            "salesperson_pos/static/src/select_salesperson_dialog/select_salesperson_dialog.js",
            "salesperson_pos/static/src/select_salesperson_dialog/select_salesperson_dialog.xml",
        ],
    }, 
    "installable": True,
    "application": True,
    "auto_install": ["point_of_sale"],
}
