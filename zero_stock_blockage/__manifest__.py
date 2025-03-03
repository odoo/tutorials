# -*- coding: utf-8 -*-

{
    'name': "Zero Stock Blockage",
    'description':
        "Allow confirmation of the sales order only if it is approved by the manager."
    ,
    'category': 'Sales',
    'depends': ['sale_management'],
    'data':[
        'views/sale_order_views.xml'
    ],
    'installable': True,
    'license': "LGPL-3"
}
