{
    'name': 'New Product Type',
    'author': 'Aditi Pawar(adpaw)',
    'license': 'LGPL-3',
    'summary': 'Sell products as kits without Manufacturing or BoM',
    'depends': [
        "sale", "product", "account"
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/product_views.xml',
        'views/sale_order_line_views.xml',
        'views/sale_kit_wizard_views.xml',
        'report/invoice_report.xml',
        'report/sale_order_portal_report.xml',
        'report/sale_order_report.xml'
    ],
    'installable': True,
    'auto_install': True
}
