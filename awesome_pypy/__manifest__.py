# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'pypy',
    'version': '1.0',
    'category': 'Tutorials/pypy',
    'sequence': 6,
    'summary': 'Mitchel admin fan here!',
    'description': """
        This module manages mitchel admin fan club
        ======================================

        Rich and fun club to join!!
    """,
    'depends': ['base'],
    'data': [
        'views/club.xml',
    ],
    'demo':[
        'data/club.xml',
    ],
    'application': True,
    'installable': True,
    'assets': {
        'static/MSI_MPG.jpg'
    },
    'license': 'OEEL-1',
}
