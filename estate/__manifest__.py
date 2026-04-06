{
    'name': 'RealEstate',
    'version': '1.0',
    'category': 'Real Estate/Brokerage',
    'summary': 'A module to manage real estate advertisements and property offers',
    'description': """A simple module to manage real estate ads.List your properties, track details like bedrooms and garden,let buyers make offers, and accept or reject them.""",
    'author': 'Pranjali Sangavekar(prsan)',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offers_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tags_views.xml',
        'views/estate_menus.xml',
    ],
    'demo': [
        'demo/estate_property_data.xml',
    ],
    'application': True,
}
