{
    'name': 'RealEstate',
    'version': '0.1',
    'summary': 'Tracks RealEstate property and buyer offers',
    'description': "Tracks RealEstate property and buyer offers",
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_menus.xml',
    ],
    'application': True,
}
