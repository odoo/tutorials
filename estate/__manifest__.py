{
    'name': 'estate',
    'depends': ['base'],
    'application': True,
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
    'data': [
        'security/ir.access.csv',
        'views/estate_menus.xml',
        'views/estate_property_offers_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_views.xml',
    ],
}
