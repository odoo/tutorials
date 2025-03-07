{
    'name': "Self Order Details",
    'depends': ['pos_restaurant'],
    'installable': True,
    'license': 'LGPL-3',
    'data': [
        'views/product_template.xml',
    ],
    "assets": {
        "pos_self_order.assets": [
            "odoo_self_order_details/static/src/components/**/*",
        ],
    }
}
