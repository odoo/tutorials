{
    'name' : 'Extended Webshop Description',
    'description' : """
        This module adds an "Ecommerce Extended Description" field to the product template.
        - Supports translations.
        - Displays on the product page in eCommerce.
        - Included in export/import functionality.
    """,
    'version' : '0.1',
    'category' : 'Website',
    'author' : 'Sudhirkumar Sharma',
    'website': "https://www.odoo.com",
    'depends' : [
        'base',
        'website_sale',
    ],
    'data' : [
        'views/template.xml',
        'views/product_views.xml',
    ],
    'installable': True,
    'application' : False,
    'license': 'LGPL-3',
}
