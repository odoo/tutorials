{
    "name": "New Product Kit",
    "version": "1.0",
    'author': "Ruchita Gothi (Rugot)",
    "depends": ["sale", "product", 'account'],
    "data": [
        'security/ir.model.access.csv',
        "views/product_views.xml",
        "views/sale_order_line_views.xml",
        "views/kit_wizard_views.xml",
        "report/sale_order_report.xml",
        "report/invoice_report.xml",
        "report/sale_order_portal_report.xml",

    ],
    "installable": True,
    'license': 'LGPL-3',
}
