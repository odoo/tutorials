{
    'name': 'Real Estate Account',
    'description': "This module allows managing property invoice.",
    'author': 'Sudarshan Maity (sumai)',
    'website': '',
    'category': 'Real Estate',
    'version': '1.0',
    'license': 'LGPL-3',
    'depends': [
        'estate',
        'estate_event',
        'account',
        ],

    'data': [
        'views/estate_property_views.xml',
    ],

    'installable': True,
}
