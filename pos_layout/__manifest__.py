{
    'name': 'POS Layout Customization',
    'version': '1.0',
    'depends': ['point_of_sale'],
    'author': 'kame',
    'category': 'Point of Sale',
    'summary': 'Customizes POS settings layout',
    'description': 'Customizes POS settings layout for three different views',
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_settings_views.xml',
        'views/report_templates.xml',
        'wizard/pos_receipt_preview_wizard.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_layout/static/src/**/*',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
