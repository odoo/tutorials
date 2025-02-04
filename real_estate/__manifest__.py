{
    'name': "Real Estate Module",

    'summary': """
        Starting module for Real Estate Project"
    """,

    'description': """
        Starting module for Real Estate Project Description
    """,

    'author': "Odoo",
    'website': "https://www.odoo.com/",
    'category': 'Tutorials',
    'version': '0.1',
    'application': True,
    'installable': True,
    'depends': ['base'],

    'data': [
        'security/security_groups.xml',
        'security/real_estate.model.access.csv'
    ],
    'assets': {
    },
    'license': 'AGPL-3'
}
