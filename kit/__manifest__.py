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
    'auto_install':True,
    'assets': {
        'web.assets_backend': [
            'kit/static/src/css/kit_styles.css',
            'kit/static/src/js/kit_sale_order_line_readonly.js',
        ],
    },
}
