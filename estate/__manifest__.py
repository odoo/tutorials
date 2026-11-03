{  # noqa: B018
    'name': "Real Estate",

    'summary': """
        Real Estate module for "Server framework 101, chapter 2: A New Application"
    """,

    'description': """
        Real Estate module for "Server framework 101, chapter 2: A New Application"
    """,

    'author': "Dimitris Mystriotis",
    'website': "https://www.odoo.com/",
    'category': 'Real Estate/Brokerage',
    'version': '0.1',
    'application': True,
    'installable': True,
    'depends': ['base', 'web'],

    'data': [
        'security/security.xml',
        'security/ir.access.csv',

        'report/estate_property_templates.xml',
        'report/estate_property_reports.xml',
        'report/res_users_templates.xml',

        'views/test_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/res_users_views.xml',
        'views/estate_menus.xml',

        'data/estate_property_type_data.xml',
    ],
    'demo': [
        'demo/estate_property_data.xml',
        'demo/estate_property_offer_data.xml',
    ],
    'assets': {

    },
    'license': 'AGPL-3'
}
