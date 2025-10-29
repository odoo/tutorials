{
    "name": "Book Price Pricelist",
    "version": "1.0",
    "author": "gasa",
    "license": "LGPL-3",
    "depends": ["sale"],
    "application": True,
    "installable": True,
    'data': {
        'views/sales_order_lines_views.xml',
        'views/account_move_lines_views.xml'
    }
}
