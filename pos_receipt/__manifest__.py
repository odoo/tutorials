{
    'name': 'POS Receipt',
    'depends': ['point_of_sale'],
    'description':"This module allows users to configure and customize POS receipt layouts.Supported layouts: Light, Boxes, and Lined.",
    'data': [
        "views/res_config_settings_form_inherit.xml",
        "wizard/pos_receipt_layout.xml",
        "security/ir.model.access.csv",
        "views/lined_layout.xml",
        "views/boxed_layout.xml",
        "views/light_layout.xml",
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_receipt/static/src/**/*',
        ],
    },
    'test': [
        'tests/test_pos_receipt',  
    ],
    'license': 'LGPL-3',
}
