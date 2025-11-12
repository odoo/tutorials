{
    'name': "Add Pricelist Price",
    'version': "1.0",
    'author': "sujal_asodariya",
    'summary': "Add Book Price",
    'depends': ["sale_management", "account"],
    'data' : [
        "views/account_move_line_views.xml",
        "views/sale_order_line_views.xml"
    ],
    'installable': True,
    'application': True,
    "license": "LGPL-3",
}
