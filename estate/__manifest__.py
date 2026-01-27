# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Real Estate',
    'version': '1.9',
    'category': 'Real Estates',
    'summary': 'Manage real estate operations',
    'author': 'Haroune Hassine',
    'license': 'LGPL-3',
    'depends': [
        'base_setup',
    ],
    'application': True,
    'installable': True,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_menus.xml',
    ],
}
