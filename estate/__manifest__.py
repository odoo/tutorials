{
    'name': 'Real Estate',
    'category': 'Tutorials',
    'depends': [
        'base'
    ],
    'application': True,
    'installable': True,
    'data': [
        'security/ir.model.access.csv',

        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_types_views.xml',
        'views/estate_property_tags_views.xml',
        'views/res_user_views.xml',
        'views/estate_menus.xml',
    ],
    'author': 'Odoo S.A.',
    'license': 'AGPL-3'
}
