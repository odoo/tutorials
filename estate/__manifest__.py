{
    'name': 'Real Estate',
    'version': '1.0',
    'description': 'anything',
    'summary': 'anything again',
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_res_users_views.xml',
        'views/estate_menus.xml',
    ],
    'depends': [
        'base',
    ],
    'application': True,
    'installable': True,
    'license': 'AGPL-3'
}
