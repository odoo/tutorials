{
    'name': "Booked Price",
    'version': "1.0",
    'description': """ ADD PRICELIST PRICE """,
    'sequence': 1,
    'depends': ["sale", "account"],
    'data': [
        "views/pricelist_account_move_views.xml",
        "views/pricelist_sale_order_views.xml"
    ],
    'installable': True,
    'application': True,
    'license': "AGPL-3"
}
