{
    'name': 'Zero Stock Approval',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Adds a Zero Stock Approval field in Sale Order',
    'description': 'This module adds a boolean field "Zero Stock Approval" to Sale Order, read-only for sales users but editable for administrators.',
    'depends': ['sale_management','stock'],
    'data': ['views/sale_order_view.xml'
    ],
    'installable': True,
    'application': False,
    }
