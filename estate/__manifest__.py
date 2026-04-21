# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Real Estate',
    'version': '19.0.0.1.0',
    'category': 'Real Estate/Properties',
    'sequence': 15,
    'summary': 'Track leads and close opportunities',
    'website': 'https://www.odoo.com/app/estate',
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_type_views.xml',
        'views/estate_property_tags_views.xml',
        'views/estate_property_users_views.xml',
        'views/estate_property_offers_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_menu.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'assets': {},
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
