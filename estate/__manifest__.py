{
    'name': 'Real Estate',
    'version': '1.0',
    'depends': ['mail'],
    'author': 'matd',
    'category': 'Real Estate/Brokerage',
    'description': """
It provides real estate module
""",
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/res_users_views.xml',
        'views/estate_property_menus.xml',
        'data/estate_property_sequence.xml',
        'data/estate.property.type.csv',
    ],
    'demo': [
        'demo/estate_property_demo.xml',
        'demo/estate_property_offer_demo.xml',
        'data/mail_message_subtype_data.xml', 
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
