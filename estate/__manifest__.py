{
    'name': 'Estate',
    'version': '0.1',
    'summary': 'First Odoo app. Manages real estate advertisement',
    'depends': [
        'base'
    ],
    'data': [
        'security/ir.access.csv',

        'views/estate_property_tag_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml'
    ],
    'application': True,
    'author': 'mabes',
    'license': 'LGPL-3',
}
