# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Estate',
    'version': '1.0',
    'summary': 'Sell real estate',
    'depends': [
        'base',
    ],
    'data': [
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_menu_views.xml',

        'security/ir.access.csv',
    ],
    'application': True,
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
