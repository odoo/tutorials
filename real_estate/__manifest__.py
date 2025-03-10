{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "Ajay Karma",
    'category': 'sales',
    'description': "Real_estate_app",
    'installable': True,
    'application': True,
    'auto-install': True,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type.xml',
        'views/estate_property_tag.xml',
        'views/estate_property_offer.xml',
        'views/estate_menus.xml',
            ]
}