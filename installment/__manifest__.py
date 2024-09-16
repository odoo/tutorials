{
    'name': 'installment',
    'version': '1.0',
    'description': 'A module for installment',
    'category': 'sales',
    'author': 'YASP',
    'sequence': 1,
    'depends': ['base', 'sale_subscription', 'account'],
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'wizard/wizard_view.xml',
        'data/installment_data.xml',
        'views/res_config_settings_view.xml',
        'views/add_emi_view.xml'
    ],
    'installable': True,
    'application': True,
}
