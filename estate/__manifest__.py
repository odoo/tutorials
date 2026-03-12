{
    'name': 'Real Estate',
    'summary': 'Manage real estate properties and offers',
    'description': "This module allows managing property advertisements,including property details, offers, and related data.",
    'author': 'Sudarshan Maity (sumai)',
    'website': '',
    'category': 'Real Estate',
    'version': '1.0',
    'license': 'LGPL-3',

    'depends': [
        'base',
        ],

    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ],

    'installable': True,
    'application': True,
}
