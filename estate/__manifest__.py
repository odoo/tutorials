# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Estate',
    'version': '1.0',
    'category': 'Sales/Estate',
    'sequence': 15,
    'summary': 'Track all the properties you own',
    'website': 'https://www.odoo.com/app/estate',
    'depends': [
        'base'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml'
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'assets': {
    },
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
