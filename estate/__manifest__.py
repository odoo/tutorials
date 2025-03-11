{
    'name': 'estate',
    'version': '1.0',
    'summary': "A comprehensive real estate management solution.",
    'description': """The Estate Management module provides an efficient way to manage properties, offers, property types, and tags. 
        It includes user access control, property status tracking, and an intuitive interface for managing real estate operations.""",
    'category': 'Tools',
    'author': 'Abhishek Patel',
    'license': 'LGPL-3',
    'depends': ['base'],
    'installable': True,
    'application': True,

    # This data field loads all required files to run the module
    'data': [
        'security/ir.model.access.csv',
        'views/estate_menus.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/res_user_views.xml',
    ],
}
