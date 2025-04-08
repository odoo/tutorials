{
    'name': 'Product Kit',
    'Category': 'Sales/Product Kit',
    'license': 'LGPL-3',
    'installable': True,
    'depends': ['sale_management', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/wizard_product_kit_views.xml',
        'views/product_template_views.xml',
        'views/sale_order_views.xml',
        'views/sale_portal_template.xml',
        'views/report_invoice.xml',
    ]
}
