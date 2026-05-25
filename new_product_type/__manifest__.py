{
    "name": "New Product Type",
    "version": "1.0",
    'author': "habar",
    "depends": ["sale", "product", 'account'],
    "data": [
        'security/ir.model.access.csv',
        "report/sale_order_portal_report.xml",
        "report/sale_order_report.xml",
        "views/product_kit_wizard_views.xml",
        "views/product_views.xml",
        "report/invoice_report.xml",
        "views/sale_order_line_views.xml",
    ],
    "installable": True,
    'license': 'LGPL-3',
}
