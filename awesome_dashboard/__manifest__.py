# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Awesome Dashboard",
    'summary': """
        Starting module for "Discover the JS framework, chapter 2: Build a dashboard"
    """,
    'description': """
        Starting module for "Discover the JS framework, chapter 2: Build a dashboard"
    """,
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
            'awesome_dashboard/static/src/**/*',
            ('remove', 'awesome_dashboard/static/src/dashboard/**/*'),
        ],
        'awesome_dashboard.dashboard': [
            'awesome_dashboard/static/src/dashboard/**/*',
        ],
    },
    'license': 'AGPL-3'
}
