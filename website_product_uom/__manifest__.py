# -*- coding: utf-8 -*-

{
    'name': 'Website Product UoM',
    'version': '1.0',
    'category': 'Website',
    'summary': 'Adds a separate UoM field for products displayed on the website',
    'author': 'Maan Patel',
    'depends': ['stock', 'website_sale'],
    'description': """
        This module introduces a Website UoM field in product templates, allowing a different
        unit of measure to be displayed on the website compared to the main UoM used in inventory.
    """,
    'data': [
        'views/product_template_views.xml',
        'views/templates.xml'
    ],
    'assets': {
        'web.assets_frontend': [
            'website_product_uom/static/src/js/website_sale.js'
        ]
    },
    'license': 'LGPL-3',
    'application': False,
    'installable': True
}
