{
    'name': 'Product Kit',
    'license': 'LGPL-3',
    'depends': [
        'sale',
        'product',
    ],
    'data': [
        "security/ir.model.access.csv",
        'wizard/product_kit_wizard_views.xml',
        'report/report_invoice.xml',
        'views/product_template_views.xml',
        'views/sale_order_views.xml',
    ],
    'installable': True,
}
