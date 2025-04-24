# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Real Estate',
    'application': True,
    'data': [
        'security/ir.model.access.csv',

        'views/estate_property_views.xml',
        'views/estate_property_tags_view.xml',
        'views/estate_property_offer_view.xml',
        'views/estate_property_types_views.xml',
        'views/res_users_views.xml',
        'views/estate_menu.xml',
    ],
    'license': 'OEEL-1',
    'depends': [
        'base',
    ],
}
