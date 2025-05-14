{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['mail'],
    'author': "Shivraj Bhapkar",
    'category': 'Real Estate/Brokerage',
    'description': 'This test module',
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/res_users_views.xml',
        'views/estate_menus.xml',
        'data/master_data.xml',
    ],
    'demo': [
        'demo/demo_data.xml',
    ],
    'installable': True,
    'application':True
}
