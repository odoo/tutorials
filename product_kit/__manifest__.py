{
    "name": "Product Type",
    "version": "1.0",
    "depends": ["sale_management","point_of_sale"],
    "application": True,
    "installable": True,
    "data": [
        "security/ir.model.access.csv",
        "wizard/sub_products.xml",
        "views/product_view.xml",
        "views/sale_order_view.xml", 
        "report/report_order_lines.xml",
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'product_kit/static/src/**/*',
        ],
    },
    "license": "AGPL-3"
}