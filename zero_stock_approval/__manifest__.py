
{
    'name': "Zero Stock Approval",
    'version': '1.0',
    'depends': [
        'base',
        'sale',
        'sales_team',
        'account_payment',
        'utm',
    ],
    'author': "Sanket Tank",
    'category': 'Sales/Sales',
    'description': """
    This module contains feature of zero stock blockage for Sales Module
    """,
    "data": [
        "views/sale_order_views.xml",
    ],
    'license': 'LGPL-3',
    'application': True,
    'installable': True
}
