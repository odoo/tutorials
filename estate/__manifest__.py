{
    'name': "Real Estate",
    'depends': ['base'],
    'application': True,
    'author': "Jeanne Delneste",
    'category': "Real Estate/Brokerage",
    'license': "LGPL-3",
    'data': [
        'views/estate_property_views.xml',
        'views/estate_property_user_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menus.xml',
        'data/estate.property.type.csv',
        'security/ir.model.access.csv',
        # 'security/security.xml'
    ],
    'demo': [
        'demo/estate_property_demo.xml',
        'demo/estate_property_offer_demo.xml',
        'demo/estate_property_type_demo.xml',
    ]
}
