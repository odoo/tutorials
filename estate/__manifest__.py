{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "Rajat",
    'category': 'Real Estate/Brokerage',
    'description': """ Description text""",
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_offer_views.xml',
        'views/estate_property_tags_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_views.xml',
        'views/inherited_view.xml',
        'security/security.xml',
        'views/estate_menus.xml',
    ],
    'demo': [
        'demo/estate.property.type.csv',
        'demo/estate_property_data.xml',
    ],
    'application': True,
    'installable': True
}
