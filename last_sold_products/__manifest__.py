{
    "name": "last sold product",
    "version": "1.0",
    "description": "show the last invoiced product first",
    "license": "LGPL-3",
    "author": "abpa",
    "category": "sale/last invoiced product",
    "depends": ["sale_management", "purchase", "stock"],
    "data": [
       'views/product_kanban_catalog_views.xml',
    ],
    'installable': True,
}
