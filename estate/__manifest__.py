{
    'name': "Estate",
    'version': '1.0.0',
    'summary': "A real estate management module for handling properties, types, and tags.",
    'description': """
        The Estate module provides functionalities for managing real estate properties, 
        property types, and property tags. It includes user access controls, views, and 
        menus for easy navigation and management.
    """,
    'license': 'LGPL-3',
    'depends': ['base','mail'],
    'category': 'Real Estate/Brokerage',
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml', 
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_menus.xml',
        'views/res_users_views.xml',
        'data/estate.property.type.xml',
    ],
    'demo':[
        'demo/estate.property.xml',
        'demo/estate.property.offer.xml',
    ],
}
