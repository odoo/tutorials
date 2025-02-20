{
    'name': "Real Estate",
    'summary': "Manage real estate properties.",
    'description': "This is the real estate module used for buying and selling properties!",
    'version': '0.1',
    'application': True,
    'category': "Real Estate/Brokerage",
    'installable': True,
    'depends': ['base','mail'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        'views/res_user_views.xml',
        'views/estate_property_offer_views.xml',
        'data/property_types.xml',
        'demo/estate_property_demo_data.xml',
        'demo/estate_property_offers_demo_data.xml',
        'data/cron.xml',
    ],
    'license': 'AGPL-3'
}
