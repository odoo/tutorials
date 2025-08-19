# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Product Warranty',
    'version': '1.0',
    'depends': ['sale_management','stock', 'website_sale'],
    'author': 'Odoo',
    'website': 'https://www.odoo.com/',
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
    'description': '''
    Product Warranty
    ''',
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_views.xml',
        'views/product_warranty_views.xml',
        'views/product_warranty_menus.xml',
        'wizard/product_warranty_wizard_view.xml',
        'views/sale_order_line_view.xml',

    ],
}
