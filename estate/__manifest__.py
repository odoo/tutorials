# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Real Estate',
    'version': '0.1',
    'category': 'Tutorials',
    'sequence': 1,
    'summary': 'Real Estate module',
    'depends': ['base'],
    'data': [
        'security/ir.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml'
    ],
    'assets': {},
    'installable': True,
    'application': True,
    'author': 'Glineur Loïc',
    'license': 'AGPL-3',
}
