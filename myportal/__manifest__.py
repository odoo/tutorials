# -*- coding: utf-8 -*-
{
    'name': "supplier_portal",

    'summary': """
        supplier portal TASK - demo task"
    """,

    'description': """
        supplier portal TASK - demo task"
    """,

    'author': "Odoo",
    'website': "https://www.odoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'supplier_portal',
    'version': '0.1',

    'depends': ['base', 'web'],
    'application': True,
    'installable': True,
    'data': [
        'views/templates.xml',
        
    ],
     'assets': {
        'myportal.assets_playground': [
            ('include', 'web._assets_helpers'),
            ('include', 'web._assets_backend_helpers'),
            'web/static/src/scss/pre_variables.scss',
            'web/static/lib/bootstrap/scss/_variables.scss',
            'web/static/lib/bootstrap/scss/_maps.scss',
            ('include', 'web._assets_bootstrap'),
            ('include', 'web._assets_core'),
            'web/static/src/libs/fontawesome/css/font-awesome.css',
            'myportal/static/src/**/*',
        ],
    },
    'license': 'AGPL-3'
}
