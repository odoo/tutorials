{
    'name': "Real Estate",

    'summary': """
        Real Estate Tuto"
    """,

    'description': """
        Starting tutorial real estate"
    """,

    'author': "Odoo",
    'website': "https://www.odoo.com/",
    'category': 'Tutorials',
    'version': '0.1',
    'application': True,
    'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        'views/estate_property_type_views.xml',

    ],
    'assets': {

    },
    'license': 'AGPL-3'
}
