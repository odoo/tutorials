{
    'name': 'estate',
    'version': '0.1',
    'application': True,
    'depends' : ['base_setup'],
    'data': [
        'views/res_users_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_menus.xml',
        'security/ir.model.access.csv',
    ],
    "license": "AGPL-3",
}
