{
    'name': 'estate',
    'version': '1.0',
    'summary': "A comprehensive real estate management solution.",
    'description': """The Estate Management module provides an efficient way to manage properties, offers, property types, and tags. 
        It includes user access control, property status tracking, and an intuitive interface for managing real estate operations.""",
    'category': 'Real Estate/Brokerage',
    'author': 'Abhishek Patel',
    'license': 'LGPL-3',
    'depends': ['base','mail'],
    'data': [
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/res_user_views.xml',
        'security/estate_security.xml',
        'security/ir.model.access.csv',
        'views/estate_menus.xml',   
    ],
    'demo': [
        'demo/demo_data_estate_property_type.xml',
        'demo/demo_data_estate_property.xml',
        'demo/demo_data_estate_property_offer.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
