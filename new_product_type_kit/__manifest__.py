{
    'name': 'Dev Zero Stock Blockage',
    'version': '1.0',
    'summary': 'Add a new prodcut type kit',
    'description': """
        Add kit-type products with configurable sub-products and conditional report visibility
    """,
    'author': 'Raghav Agiwal',
    'depends': ['sale_management', 'stock', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_view.xml',
        'views/sale_order_line_view.xml',
        'views/kit_wizard_views.xml',
        'views/portal_saleorder_templates.xml',
        'report/report_saleorder_templates.xml',
        'report/report_invoice_templates.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3'
}
