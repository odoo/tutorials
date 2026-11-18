{
    'name': 'Estate',
    'summary': 'Real estate module',
    'application': True,
    'installable': True,
    'author': 'Thing-odoo',
    'license': 'LGPL-3',
    'depends': [
        'base'
    ],
    'data': [
        'security/ir.access.csv',

        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_menu_views.xml',
    ],
}
