{
    'name': "Sales Kit",
    'version': '1.0',
    'depends': ['base', 'stock', 'sale_management'],
    'author': "Rajat",
    'description': """Make sale order with kit""",
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_views.xml',
        'wizard/subproduct_wizard.views.xml',
        'views/sale_order_views.xml',
        'report/ir_actions_report_templates.xml',
        'report/report_invoice.xml',
        'views/sale_portal_templates.xml'
    ],
    'application': False,
    'installable': True
}
