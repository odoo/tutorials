{
    'author': 'Odoo S.A.',
    'name': 'Purchase Discount',
    "description": """
    This module introduces a global discount feature for Purchase Orders,
    allowing users to apply either value-based or percentage-based discounts.
    """,
    'depends': ['purchase'],
    'license': 'LGPL-3',
    'data': [
        'views/purchase_order_views.xml'
    ],
    'application': True,
    'installable': True
}
