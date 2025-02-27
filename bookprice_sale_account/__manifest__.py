{
    'name': 'Book Price for Sales and Invoice',
    'version': '1.0',
    'category': 'Sales',
    'author': "Odoo S.A.",
    'summary': 'Display the Original Pricelist price (Book Price) on sales orders and invoices',
    'depends': ['sale_management'],
    'data': [
        'views/account_move_view.xml',
        'views/sale_order_view.xml',
    ],
    'auto_install': True,
    'license': 'LGPL-3'
}
