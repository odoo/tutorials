{
    'name': 'Real Estate',
    'version': '1.0',
    'depends': ['base'],
    'author': 'ATPA',
    'category': 'Real Estate/Brokerage',
    'description': """
Real Estate module is for training, the module contains property types, offers and tags.
""",
    'data' : [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/res_users_view.xml',
        'views/estate_property_menus.xml',
        'data/estate_property_sequence.xml',
        'data/estate_property_type_demo.xml',
        'data/estate_property_demo.xml',
        'data/estate_property_offer_demo.xml',
    ],
    'application' : True,
    'license' : 'LGPL-3'
}
