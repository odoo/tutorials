# -*- coding: utf-8 -*-
{
    'name': "Estate",

    'summary': """
        Tutorial starting module
    """,

    'description': """
        Tutorial starting module
    """,

    'author': "Cemal Faruk Guney",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Tutorials/Estate',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],
    'application': True,
    'installable': True,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml'
    ],
    'license': 'AGPL-3'
}
