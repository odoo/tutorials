# A custom real estate module, created for learning purposes

{
    'name': '[TUTO] Estate',
    'summary': 'Track your real estate properties',
    'depends': [
        'base_setup'
    ],
    'data': [
        'security/ir.model.access.csv',

        'views/estate_property_views.xml',
        'views/estate_settings_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_menu_views.xml'
    ],
    'installable': True,
    'application': True,
    'demo': [
        "demo/estate_demo.xml",
    ],
    'auto_install': True
}
