{
    'name': 'Real Estate',
    'version': '1.0',
    'depends': ['base'],
    'author': 'matd',
    'category': 'Category',
    'description': """
    It provides real estate module
    """,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_menus.xml',
    ],
    'application': True,
}
