{
    "name": "Point of Sale Second UoM",
    "version": "1.0",
    "summary": " provide second uom functionality",
    "description": """
        Add second UoM for the products in pos
    """,
    "author": "Odoo",
    "depends": ["point_of_sale"],
    'auto_install': True,
    'data': [
        'views/product_view.xml'
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "point_of_sale_second_uom/static/src/**/*",
        ],
        'web.assets_tests': [
            'point_of_sale_second_uom/static/tests/tours/**/*',
        ],
    },
    "license": "LGPL-3",
}
