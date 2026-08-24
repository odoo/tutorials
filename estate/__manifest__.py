# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Estate',
    'version': '0.1',
    'sequence': 99,
    'summary': 'Estate Management',
    'depends': [
        'base',
        'web',
    ],
    'installable': True,
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tags_views.xml',
        'views/res_users_views.xml',
        'views/estate_menus.xml',
    ],
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
