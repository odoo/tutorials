{
    'name': "Estate",
    'depends': ['base'],
    'application': True,
    'data': [
        'security/ir.model.access.csv',

        'views/estate_property_users.xml',
        'views/estate_property_offer_view.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_type_view.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ]
}
