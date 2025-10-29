{
    'name': "book_price_sale",
    'version': "1.0",
    'summary': "Add book_price field in sales order line and invoice order line in sales app",
    'description': """
        This module will add a button book_price in the sales order line and invoice order line in the sales app.
    """,
    'author': "priyansi borda",
    'depends': ['sale'],
    'data': [
        "view/sales_order_line_view.xml",
        "view/invoice_order_line_view.xml"
    ],
    'application': False,
    'installable': True,
    'license': 'LGPL-3',
}
