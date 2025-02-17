{
    'name': 'Real Estate',
    'version': '1.0',
    'depends': ['base'],
    'author': 'matd',
    'category': 'Real Estate/Brokerage',
    'description': """
It provides real estate module
""",
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/estate_property_sequence.xml',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/res_users_views.xml',
        'views/estate_property_menus.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
