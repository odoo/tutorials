{
    'name': "My Real Estate",
    'license': 'LGPL-3',
    'depends': ['base'],
    'installable': True,
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'views/real_estate_property_views.xml',
        'views/real_estate_property_offers_views.xml',
        'views/real_estate_property_category_views.xml',
        'views/real_estate_property_tags_views.xml',
        'views/real_estate_menus.xml',
    ]
}
