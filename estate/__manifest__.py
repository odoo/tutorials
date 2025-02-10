{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "djsh",
    'category': 'Category',
    'description': """
Real Estate Properties With all the information
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
