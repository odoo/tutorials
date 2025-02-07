{
    'name': 'installments',
    'version': '1.0',
    'author' : 'Dhruv Chauhan',
    'description': 'Installments management module!',
    'depends': ['base', 'sale'],
    'data': [
        'security/ir.model.access.csv',

        'views/sale_order_views.xml',
        'views/res_config_settings_views.xml',

        'data/product_data.xml',
        'data/ir_cron.xml',
        
        'wizard/installment_wizard.xml'
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3', 
}
