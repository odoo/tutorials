# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "stancor_customization",
    'description': "Stancor UOM and Qty Customization ",
    'author': "Odoo",
    'website': "https://www.odoo.com",
    'category': 'Product',
    'version': '0.1',
    'depends': ['sale_management', 'stock', 'account'],
    'license': 'LGPL-3',
    'data': [
        'views/product_template_form_view.xml',
        'views/sale_order_line_view.xml',
        'views/view_picking_form.xml',
        'views/report_stockinventory.xml',
        'views/view_mrp_production_form.xml',
    ],
}

