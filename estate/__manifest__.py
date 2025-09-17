# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Estate',
    'depends': [
        'base',
    ],
    'version': '19.0.0.0',
    'installable': True,
    'application': True,
    'data': [
        'views/res_users_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        'security/ir.model.access.csv',
    ],
}
