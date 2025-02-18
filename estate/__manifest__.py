{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base', 'mail'],
    'author': "djsh",
    'category': 'Real Estate/Brokerage',
    'description': """
Real Estate Properties with the information regarding buyers, sellers, properties, property offers, property types and property tags.
""",
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/mail_message_subtype.xml',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/res_users_views.xml',
        'views/estate_property_menus.xml',
    ],
    'demo':[ 
        'demo/estate_property_type_demo.xml',
        'demo/estate_property_demo.xml',
        'demo/estate_property_offer_demo.xml',
    ],
    'application': True,
    'license': 'LGPL-3',
}
