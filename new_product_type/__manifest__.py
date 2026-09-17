{
    "name": "New Product Type",
    "version": "1.0",
    'author': "abkus",
    "depends": ["sale", "product"],
    "data": [
        "security/ir.model.access.csv",
        "views/product_kit_wizard_views.xml",
        "views/product_views.xml",
        "views/sale_order_line_views.xml",
    ],
    "installable": True,
    'license': 'LGPL-3',
}
