{
    'name': 'Mass Return For Done Transfers',
    'description': """
    This Module allows to return multiple transfers at once
    """,
    'depends': [
        'stock',
        'sale_management',
        'purchase',
    ],
    'data': [
        'wizard/stock_picking_return.xml',
    ],
    'installable': True,
    'auto_install': True,
    'license': 'LGPL-3',
}
