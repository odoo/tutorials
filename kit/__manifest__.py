{
    'name': "kit",
    'version': '1.0',
    'depends': ['sale_management'],
    'author': "odoo",
    'data': [
        'security/ir.model.access.csv',
        'wizard/sub_product_wizard.xml',
        'views/product_views.xml',
        'reports/report_invoice_template.xml',
        'views/sale_order_views.xml',
    ],
}
