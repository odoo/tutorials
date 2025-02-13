{
    'name': 'Real Estate',
    'version': '1.0',
    'depends': ['base'],
    'author': 'ATPA',
    'category': 'Category',
    'description': """
Real Estate module is for training, the module contains property types, offers and tags.
""",
    'data' : [
        'security/ir.model.access.csv',
        'views/estate_property_menus.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/res_users_view.xml'
    ],
    'application' : True,
    'license' : 'LGPL-3'
}
