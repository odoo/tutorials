{
    'name': 'estate',
    'depends': [
        'base'
    ],
    'installable': True,
    'application': True,
    'data': [
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        'views/estate_res_users.xml',
    ],
    'license': 'LGPL-3',
}
