# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Estate',
    'version': '0.1',
    'sequence': 99,
    'summary': 'Estate Management',
    'depends': [
        'base',
        'web'
    ],
    'installable': True,
    'application': True,
    'data': [
        'security/ir.model.access.csv',
    ],
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
