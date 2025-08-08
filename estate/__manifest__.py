{
    'name': 'Real Estate',
    'version': '18.0',
    'description': 'A real estate app',
    'depends': [
        'base'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        'views/estate_user_views.xml'
    ],
    'application': True,
}
