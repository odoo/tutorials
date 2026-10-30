{
    'name': 'My Real Estate',
    'author': 'Odoo S.A.',
    'category': 'Tutorials',
    'installable': True,
    'application': True,
    'depends': ['base'],
    'license': 'AGPL-3',
    'data': [
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/res_users_view.xml',
        'views/estate_menus.xml',
        'security/ir.access.csv',
    ],
}
