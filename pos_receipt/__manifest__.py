{
    'name': 'POS receipt',
    'version': '1.0',
    'author': 'niyp',
    'depends': ['point_of_sale'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/pos_receipt_wizard_views.xml',
        'views/res_config_settings_view.xml',
        'views/boxes_receipt.xml',
        'views/lined_receipt.xml',
        'views/light_receipt.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_receipt/static/src/**/*',
        ],
    },
    'installable': True,
    'license': 'LGPL-3',
}
