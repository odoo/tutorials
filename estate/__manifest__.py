{
    'name': 'Real Estate',
    'version': '1.0',
    'category': 'tutorials',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_menus.xml',
    ],
    'installable': True,
    'application': True,
    'author': 'Disha Shah(SHADI)',
    'description': """Training module for real estate""",
    'license': 'LGPL-3',
}
