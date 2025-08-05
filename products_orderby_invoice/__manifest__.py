# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Products Orderby Invoice',
    'version': '1.0',
    'depends': ['sale_management', 'account', 'stock', 'purchase'],
    'data': [
        'views/product_views.xml',
    ],
    'installable': True,
}
