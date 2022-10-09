# -*- coding: utf-8 -*-
{
    'name': "owl_playground",

    'summary': """
        Play with Owl in this playground module""",

    'description': """
        Play with Owl in this playground module
    """,

    'author': "Odoo",
    'website': "https://www.odoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Productivity',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web'],
    'application': True,
    'installable': True,
    'data': [
        'views/templates.xml',
    ],
    'assets': {
        'owl_playground.assets_playground': [
            # bootstrap
            ('include', 'web._assets_helpers'),
            'web/static/src/scss/pre_variables.scss',
            'web/static/lib/bootstrap/scss/_variables.scss',
            ('include', 'web._assets_bootstrap'),

            'web/static/src/libs/fontawesome/css/font-awesome.css', # required for fa icons
            'web/static/src/legacy/js/promise_extension.js', # required by boot.js
            'web/static/src/boot.js', # odoo module system
            'web/static/src/env.js', # required for services
            'web/static/src/session.js', # expose __session_info__ containing server information
            'web/static/lib/owl/owl.js', # owl library
            'web/static/lib/owl/odoo_module.js', # to be able to import "@odoo/owl"
            'web/static/src/core/utils/functions.js',
            'web/static/src/core/browser/browser.js',
            'web/static/src/core/registry.js',
            'web/static/src/core/assets.js',
            'owl_playground/static/src/**/*',
        ],
    }
}
