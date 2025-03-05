# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name':'',
    'version':'1.0',
    'author':'JODH',
    'description':"""
This Module provides warranty feature for Product.
""",
    'depends': ['sale_management'],
'data':[
        'security/ir.model.access.csv',
        'wizard/add_warranty_wizard_views.xml',
        'views/warranty_config_views.xml',
        'views/product_template_views.xml',
        'views/sale_order_views.xml',
        'views/warranty_config_menus.xml',
    ],
    'installable': True,
    'license':'LGPL-3',
}
