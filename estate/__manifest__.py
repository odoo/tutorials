{
    'name': 'Real Estate',
    'version': '1.0',
    'category': 'Real Estate',
    'depends': ['base'],
    'data' : [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/res_users_views.xml',
        'views/estate_menus.xml',
    ],
    'instalable': True,
    'application':True,
    'license': 'LGPL-3'
}
