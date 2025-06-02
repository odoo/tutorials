{
    'name': 'Estate',
    'category': 'Real Estate/Brokerage',
    'depends': [
        'base'
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/estate_property_views.xml',
        'views/estate_property_tag_views.xml',
        'views/res_users_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_menus.xml',
        'data/estate.property.type.csv',
    ],
    'demo': [
        'demo/estate.property_demo.xml',
        'demo/estate.property.offer_demo.xml'
    ],
    'license': 'AGPL-3'
}
