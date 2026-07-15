{
    'name': 'Real Estate',
    'depends': ['base'],
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_maintenance_views.xml',
        'views/estate_menus.xml',
        'data/data_type.xml',
        'data/data_tags.xml',
        'data/data.xml',
    ],
}
