{
    "name": "POS - Improvements",
    "version": "1.0",
    "description": "Enable direct payment from the ticket screen in POS",
    "author": "Ravij Parikh (snrav)",
    "application": True,
    "depends": ["point_of_sale"],
    "license": "LGPL-3",
     "assets": {
        "point_of_sale.assets_prod": [
            "pos_improvements/static/src/pos_ticket_screen/js/pos_ticket_screen.js",
            "pos_improvements/static/src/pos_ticket_screen/xml/pos_ticket_screen.xml"
        ],
    }
}
