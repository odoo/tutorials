{
    'name': "Add Pricelist Price",
    'version': "1.0",
    'description': """
        Module for displaying the original pricelist price (Book Price) on Sales Order Lines and Invoice Lines.
        This helps in comparing the standard pricelist price with manually adjusted prices.
    """,
    'depends': ['sale', 'account'],
    'category': "Sales",
    'author': "Himilsinh Sindha (hisi)",
    'website': "https://www.odoo.com/app/sales",
    'data': [
        'views/sale_order_view.xml',
        'views/account_move_view.xml',
    ],
    'license': "LGPL-3",
    'installable': True,
    'auto_install': False,
}
