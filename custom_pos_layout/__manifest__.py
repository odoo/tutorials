{
    'name': 'POS Custom Bill',
    'version': '1.0',
    'category': 'Point of Sale',
    'summary': 'Customizes the PoS order receipt format',
    'author': 'Your Name',
    'depends': ['point_of_sale'],
    'data' : [
        'security/ir.model.access.csv',
        'views/res_config_settings_views.xml',
        'views/report_templates.xml',
        'wizard/pos_receipt_preview_wizard.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'custom_pos_layout/static/src/**/*',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
