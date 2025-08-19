{
    'name': 'Sale Order Product History',
    'version': '1.0',
    'category': 'Sales',
    'depends': ['sale_management', 'stock', 'purchase'],
    'data': [
        'views/purchase_order_form.xml',
        'views/sale_order_form_view.xml',
        'views/product_template_kanban_catalog.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3'
}
