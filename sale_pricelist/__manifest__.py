{
    'author': 'Odoo S.A.',
    'name': 'Sale Pricelist',
    'description': """
    Add a "Book Price" field on Sales Order Lines and Invoice Lines to display the original
    pricelist price of a product. This helps users compare the standard pricelist amount
    with any manually adjusted line price, ensuring pricing transparency and better control
    over discount or custom price modifications.
    """,
    'depends': ['sale_management'],
    'license': 'LGPL-3',
    'data': [
        'views/sale_order_views.xml',
        'views/account_move_views.xml',
    ],
    'application': True,
    'installable': True
}
