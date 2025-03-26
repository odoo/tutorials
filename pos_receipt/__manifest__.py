{
    'name': 'POS Receipt Layouts',
    'category': 'Point of Sale',
    'summary': 'Customize POS receipt layouts with different LAYOUT',
    'description': '''
        This module extends the Point of Sale receipt functionality by adding:
        * Three predefined receipt layouts (Light, Box, Lined)
        * receipt preview
        * Customizable header and footer
    ''',
    'depends': ['point_of_sale'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/receipt_layout.xml',
        'views/res_config_settings_views.xml',
        'views/pos_receipt_restaurant_templates.xml',
        'views/pos_receipt_retail_templates.xml'
        
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_receipt/static/src/**/*',
    
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': True,
    'license': 'LGPL-3',
}
