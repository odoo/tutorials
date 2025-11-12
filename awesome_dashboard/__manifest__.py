# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Awesome Dashboard",
    'category': 'Tutorials/AwesomeDashboard',
    'summary': """
        Starting module for "Discover the JS framework, chapter 2: Build a dashboard"
    """,
    'description': """
        Starting module for "Discover the JS framework, chapter 2: Build a dashboard"
    """,
    'version': '0.1',
    'author': "Odoo",
    'website': "https://www.odoo.com/",
    'depends': ['base', 'web', 'mail', 'crm'],
    'data': [
        'views/views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'awesome_dashboard/static/src/component/dashboard/dashboard.js',
            'awesome_dashboard/static/src/component/dashboard/dashboard.scss',
            'awesome_dashboard/static/src/component/dashboard/dashboard.xml',
            'awesome_dashboard/static/src/services/dashboard_services.js',
            'awesome_dashboard/static/src/component/dashboardItem/dashboard_item.js',
            'awesome_dashboard/static/src/component/dashboardItem/dashboard_item.xml',
        ],
    },
    'application': True,
    'installable': True,
    'license': 'LGPL-3'
}
