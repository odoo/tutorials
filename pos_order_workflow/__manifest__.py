{
    'name': 'POS Order Workflow',
    'version': '1.0',
    'summary': 'POS Order Workflow',
    'author': 'Raghav Agiwal',
    'depends': ['point_of_sale'],
    "assets": {
        "point_of_sale._assets_pos": [
            "pos_order_workflow/static/src/*",
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': True,
    'license': 'LGPL-3'
}
