# -*- coding: utf-8 -*-
{
    'name': "Awesome Dashboard",

    'summary': """
        Starting module for "Discover the JS framework, chapter 2: Build a dashboard"
    """,

    'description': """
        Starting module for "Discover the JS framework, chapter 2: Build a dashboard"
    """,

    'author': "Odoo",
    'website': "https://www.odoo.com/",
    'category': 'Tutorials/AwesomeDashboard',
    'version': '0.1',
    'application': True,
    'installable': True,
    'depends': ['base', 'web', 'mail', 'crm'],

    'data': [
        'views/views.xml',
    ],
    'assets': {
        'web.assets_backend': [
        'awesome_dashboard/static/src/**/*.js',  # Load all JS files except lazy ones
        'awesome_dashboard/static/src/**/*.xml',  # Load all XML files
        'awesome_dashboard/static/src/scss/**/*.scss',
        ],
        'awesome_dashboard.dashboard_assets':[
            "awesome_dashboard/static/src/dashboard/**/*.js",
            "awesome_dashboard/static/src/dashboard/**/*.xml",
            # "awesome_dashboard/static/src/dashboard/scss/*.scss",
        ]
    
    },
    'license': 'AGPL-3'
}
