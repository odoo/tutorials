{
    'name': "Sale Order POS",
    'category': 'pos_restaurant',
    'version': '0.1',
    'depends': ['pos_restaurant', 'pos_self_order'],
    'sequence': 1,
    'application': True,
    'installable': True,
    'data': [
        "views/product_views.xml",
    ],
    "assets": {
        "pos_self_order.assets":
            ["odoo_self_order_details/static/src/**/*"],
    },
    'license': 'AGPL-3'
}
