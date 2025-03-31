# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Catalog",
    'category': 'Catalog/Catalog',
    'summary': "Manage and showcase product catalogs with ease.",
    'description': """
Create, categorize, and generate printable product catalogs effortlessly.
""",
    'version': '1.0',
    'author': "rsbh",
    'depends': ['product', 'sale_management', 'stock'],
    'data': [
          'security/ir.model.access.csv',
          
          'report/catalog_product_templates.xml',
          'report/catalog_product_report.xml',

          'wizard/price_list_wizard_views.xml',
          
          'views/catalog_catalog_views.xml',
          'views/catalog_menus.xml',
          'views/sale_order_views.xml',
          'views/product_views.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'catalog/static/src/**/*',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
