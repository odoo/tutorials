{
    'name': 'Product Kits',
    'version': '1.0',
    'depends': ['base', 'sale_management'],
    'author': 'Aryan Donga (ardo)',
    'description': 'Simple module to create and sell product kits',
    'application': False,
    'installable': True,
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'report/sale_order_report.xml',
        'report/report_invoice.xml',
        'report/sale_order_portal_view.xml',
        'views/product_template_views.xml',
        'wizard/product_kit_wizard_views.xml',
        'views/sale_order_views.xml'
    ],
}
