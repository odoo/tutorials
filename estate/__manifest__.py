{
    'name': 'Estate',
    'depends': ['base'],
    'category': 'Estate/Brokerage',
    'data': [
        'security/estate_security.xml',
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/res_users_views.xml',
        'views/estate_menus.xml',
        'data/estate.property.type.csv',
        'data/estate.property.tag.csv',
    ],
    'demo': [
        'demo/estate_property_demo.xml',
        'demo/estate_property_offer_demo.xml',
    ],
    'license': 'LGPL-3',
}
