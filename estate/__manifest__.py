{
    'name': "estate",
    'version': '1.0',
    'depends': ['base', 'mail'],
    'author': "srap",
    'data': [
        'security/ir.model.access.csv',
        'views/res_users_views.xml',
        'views/estate_property_offers_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tags_views.xml',
        'views/estate_menus.xml',
    ],
    "demo": [
        'data/estate.property.type.csv',
        "demo/demo_data.xml",
    ],
    'application': True
}
