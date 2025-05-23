# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Pos Product Uom",
    'category': 'Sales/Point of Sale',
    'summary': "Sell products in a secondary unit of measure in POS",
    'description': """
Module to allow cashiers to sell products using a secondary unit of measure (UOM) in the Point of Sale
""",
    'version': '1.0',
    'author': "rsbh",
    'depends': ['point_of_sale'],
    'data': [
          'views/product_template_views.xml'
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_product_uom/static/src/**/*',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
