{
    "name":'Real Estate',
    "summary": "An estate app",
    'category':'Real Estate/Brokerage',
    'depends': ['base'],
    'data':[
        'security/estate_security.xml',
        'security/ir.model.access.csv',
        'views/estate_property_tags_view.xml',
        'views/estate_property_offer_view.xml',
        'views/estate_property_type_view.xml',
        'views/estate_property_res_users.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml'
    ],
    'installable': True,
    'application': True,
    "license":"LGPL-3"
}
