{
    'name': 'Real Estate',
    'depends': [
        'base'
    ],
    'application': True,
    'data': [
        'views/estate_property_tag_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_menus.xml',
        'views/estate_property_views.xml',
        'security/ir.access.csv',
    ],
    'author': 'Odoo S.A.',
    'license': 'OEEL-1',
}
