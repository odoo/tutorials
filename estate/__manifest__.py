{
    'name': 'Real Estate',
    'version': '1.0',
    'description': """
    Real Estate Management
    """,
    'depends': [
        'base',
    ],
    'data': [
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menus.xml',
        'views/res_users_views.xml',
        'security/ir.model.access.csv',
    ],
    'application': True,
    'license': 'LGPL-3',
}
