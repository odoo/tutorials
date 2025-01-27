{
    'name' : "Real Estate",
    'depends' : ['base'],
    'application': True,
    'data' : [
        'security/ir.model.access.csv',
        'views/estate_property_offer.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag.xml',
        'views/estate_property_users_views.xml',
        'views/estate_menus.xml',
    ]
}