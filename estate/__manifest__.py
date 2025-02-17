{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "djsh",
    'category': 'Real Estate/Brokerage',
    'description': """
Real Estate Properties with the information regarding buyers, sellers, properties, property offers, property types and property tags.
""",
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_menus.xml',
        'views/res_users_views.xml',
        'data/ir_sequence_data.xml',
        'data/estate_property_type_demo.xml',
        'data/estate_property_demo.xml',
    ],
    'license': 'LGPL-3',
    'application': True,
}
