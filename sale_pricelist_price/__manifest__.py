{
    'name': "Add Pricelist Price",
    'version': "1.0",
    'depends': ["sale_management"],
    'category': 'Sales/Sales',
    'description': """
    This is the add-on module that enables 'Book Price' field into order lines of
    Sales Orders and Invoicing to let the client know of actual price and adjusted price.
    """,
    'installable': True,
    'license': "LGPL-3",

    'data': [
        "views/sale_order_line_views.xml",
        "views/account_move_line_views.xml",
    ],

}
