{
    'name': 'Installement App',
    'version': '17.0',
    'depends': ['base', 'sale_subscription'],
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'wizard/add_emi_button_wizard_views.xml',
        'views/add_emi_button_views.xml',
        'views/res_config_settings_views.xml',
        'data/data.xml',
        'data/penalty_installement.xml'
    ],
    'installable': True,
    'application': True,
}
