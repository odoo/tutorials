{
    'name': 'Estate',
    'version': '1.0',
    'author': 'Odoo S.A.',
    'license': 'AGPL-3',
    'installable': True,

    'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_offers_views.xml',
        'views/estate_property_types_views.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        'views/res_users_views.xml'
    ]
}
