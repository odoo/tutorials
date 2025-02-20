{
    'name': "Real Estate",
    'summary': "Starting module for Real Estate Project",
    'description': "Starting module for Real Estate Project Description",
    'category': 'Real Estate/Brokerage',
    'application': True,
    'installable': True,
    'depends': [
        'base',
        'mail'
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/res_users_views.xml',
        'views/estate_property_menu_views.xml',
        'data/estate_property_type_data.xml',
        'demo/estate_property_demo.xml',
        'demo/estate_property_offer_demo.xml',
        'data/cron.xml'
    ],
    'license': 'AGPL-3'
}
