{
    'name': 'Self Order Product Details',
    'version': '1.0',
    'description': 'Open custom dialog on product click',
    'depends': ['pos_self_order'],
    'assets': {
        "pos_self_order.assets": [
            'odoo_self_order_details/static/src/**/*'
        ],
    },
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False
}
