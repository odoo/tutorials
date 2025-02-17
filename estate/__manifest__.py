{
    'name': "Real Estate",
    'depends': ['base', 'mail'],
    'author': "Ayush Kumar Singh",
    'application': True,
    'data': [
        'data/ir.model.access.csv',
        'views/estate_property_offer_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/res_users_views.xml', 
        'views/estate_menus.xml',
    ],
    'license': 'LGPL-3'                                   # default LGPL-3 but if not specified then we get warning in terminal 
}
