{
    'name': "pos formate",
    'version': '1.0',
    'depends': ['point_of_sale'],
    'author': "gasa",
    "license": "LGPL-3",
    "sequence": 1,
    'data': [
        'security/ir.model.access.csv',
        'wizards/pos_configure_receipt_views.xml',
        'views/res_config_settings_views.xml',
        'views/boxed_template.xml',
        'views/lined_template.xml',
        'views/light_template.xml',
    ],
    'installable': True,
    'application': True,
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_formate/static/src/order_receipt_patch.js',
            'pos_formate/static/src/order_receipt_patch.xml',
        ],
    },
}
