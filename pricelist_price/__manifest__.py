{
    'name': "Booked Price",
    'version': "1.0",
    'description': "ADD PRICELIST PRICE",
    'sequence': 1,
    'depends': ["sale_management", "account"],
    'data': [
        "views/account_move_views.xml",
        "views/sale_order_views.xml"
    ],
    'installable': True,
    'application': True,
    'license': "LGPL-3"
}
