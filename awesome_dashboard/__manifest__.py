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
    'category': 'Tutorials',
    'version': '0.1',
    'application': True,
    'installable': True,
    'depends': ['base', 'web', 'mail', 'crm'],

    'data': [
        'views/views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'awesome_dashboard/static/src/dashboard_action.js',
        ],
        'awesome_dashboard.dashboard': [
            'awesome_dashboard/static/src/dashboard_items_service.js',
            'awesome_dashboard/static/src/dashboard_items.js',
            'awesome_dashboard/static/src/dashboard/**/*.js',
            'awesome_dashboard/static/src/dashboard/**/*.xml',
            'awesome_dashboard/static/src/piechart/**/*.js',
            'awesome_dashboard/static/src/piechart/**/*.xml',
            'awesome_dashboard/static/src/dashboard_item/**/*.js',
            'awesome_dashboard/static/src/dashboard_item/**/*.xml',
            'awesome_dashboard/static/src/dashboard_configuration_dialog.js',
            'awesome_dashboard/static/src/dashboard_configuration_dialog.xml',
            'awesome_dashboard/static/src/statistics_service.js',
            'awesome_dashboard/static/src/dashboard.scss',
        ],
    },
    'license': 'AGPL-3'
}
