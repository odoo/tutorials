# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'estate account',
    'version': '1.0',
    'summary': 'Added Real estate account module',
    'description': """
        Real Estate Account Management Module
        =============================
        Manage properties, offers, and real estate transactions.
    """,
    'depends': [
        'base_setup',
        'estate',
        'account'
    ],
    'author': 'Muhammad Qasim Shabbir',
    'license': 'LGPL-3',
    'category': 'Real Estate',

    # Required for Odoo 18
    'installable': True,
    'application': True,
    'auto_install': False,

}

