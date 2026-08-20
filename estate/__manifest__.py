{
    'name': 'Real Estate',
    'version': '0.1',
    'sequence': 100,
    'summary': 'Real Estate Advertisement',
    'depends': [
        'base'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/res_users_views.xml',
        'views/estate_menus.xml'
    ],
    'installable': True,
    'application': True,
    'assets': {},
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
