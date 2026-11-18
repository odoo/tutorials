# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Real Estate',
    'depends': [
        'base'
    ],
    'application': True,
    'data': [
        'views/estate_property_tag_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_menus.xml',
        'views/estate_property_views.xml',
        'security/ir.access.csv',
    ]
}
