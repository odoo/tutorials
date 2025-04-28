{
    'name': 'Real Estate',
    'depends':
        ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_views.xml',
        'views/res_users_views.xml',
        'views/estate_menu.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'AGPL-3',
}
