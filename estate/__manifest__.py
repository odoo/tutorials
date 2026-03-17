# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'estate',
    'category': 'Tutorials',
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ],
    'application': True,
    'installable': True,
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',

}
