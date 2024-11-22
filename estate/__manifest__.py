{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base'],
    'category': 'Training',

    'data': [
        'security/estate_groups.xml',
        'security/ir.model.access.csv',
        'security/estate_security.xml',

        # views
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/res_users_views.xml',

        # menu
        'views/estate_menus.xml',

    ],
    'application': True,
    'license': 'AGPL-3',
}
