# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Website Uom",
    'version': '1.0',
    'depends': ['sale_management', 'uom', 'website_sale', 'sale_loyalty'],
    'author': "Raj Pavara",
    'description': """
Module for adding products to the cart according to the website's UOM field.
    """,
    'application': True,
    'license': 'LGPL-3',
    'data': [
        'views/product_template_views.xml',
        'views/templates.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'sale/static/src/js/product/*',
            'sale/static/src/js/quantity_buttons/*',
        ],
        'web.assets_frontend': [
            ('before', 'website_sale/static/src/js/website_sale.js', 'website_uom/static/src/js/sale_variant_mixin.js'),
            'website_uom/static/src/js/website_sale.js',
            'website_uom/static/src/js/product_configurator_dialog/*'
        ],
    }
}
