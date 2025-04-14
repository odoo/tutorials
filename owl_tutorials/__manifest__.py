# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "owl_tutorials",
    'description': """
    odoo owl tutorials practice
    """,
    'author': "Odoo",
    'website': "https://www.odoo.com",
    'license': 'LGPL-3',
    'version': '1.0',
    'depends': ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'owl_tutorials/static/src/components/**/*',
        ],
    },
    'installable': True,
    'application': True,
}
