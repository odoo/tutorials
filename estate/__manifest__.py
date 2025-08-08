{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base','mail'],
    'author': "malh",
    'description': """
    Real estate tutorial application
    """,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/res_user_views.xml',
        'views/estate_menus.xml',
    ],
    'license': 'LGPL-3',
}
