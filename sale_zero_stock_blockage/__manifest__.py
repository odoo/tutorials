{

    'name' : "Sales zero stock blockage",
    'version' : "1.0",
    'category': 'Sales/Sales',
    'description': """
        This module add zero stock blockage feature in sale module.
    """,
    'depends': [
        'sale_management',
        'sales_team'
    ],
    'data': [
        'views/sale_order_views.xml'
    ],
    'license': 'LGPL-3'
}
