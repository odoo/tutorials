{
    'name': 'Sale Order Zero Stock Approval',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Adds a Zero Stock Approval boolean field to Sale Orders.',
    'description': 'Adds a new boolean field Zero Stock Approval in Sale Orders with access restrictions.',
    'author': 'Shiv Bhadaniya',
    'depends': ['sale_management'],
    'data': [
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
