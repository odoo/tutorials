{
    'name': 'Estate',
    'category': 'Real Estate/Brokerage',
    'depends': [
        'base'
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/estate_security.xml',

        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/res_users_views.xml',
        'views/estate_menus.xml'
    ],
    'demo': [
        'demo/estate_property_type_data.xml',
        'demo/estate_property_data.xml',
        'demo/estate_property_offer_data.xml',
    ],
    'application': True
}
