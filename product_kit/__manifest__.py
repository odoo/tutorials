{
    "name": "Product kit",
    "depends": ["sale_management"],
    "author": "Amit Gangani",
    "category": "Product/Product kit",
    "data": [
        "security/ir.model.access.csv",
        "report/sale_portal_templates.xml",
        "report/ir_actions_report_templates.xml",
        "wizard/sub_product_wizard_views.xml",
        "views/product_views.xml",
        "views/sale_order_views.xml"
    ],
    "assets": {
        "web.assets_backend": [
            'product_kit/static/src/**/*',
        ]
    },
    "installable": True,
    "application": True,
    "auto_install": False,
    "license": "LGPL-3", 
}
