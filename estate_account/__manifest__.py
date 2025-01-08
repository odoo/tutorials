# -*- coding: utf-8 -*-
{
    'name': "estate_account",

    'summary': """
        Starting module for "Discover the JS framework, chapter 1: Owl components"
    """,

    'description': """
        Starting module for "Discover the JS framework, chapter 1: Owl components"
    """,

    'author': "Odoo",
    'website': "https://www.odoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Tutorials/estate',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web','estate','account'],
    'application': True,
    'installable': True,
    'data' : [
        


    ],
   
    'license': 'AGPL-3'
}
