{
    'name': "Real Estate",

    'summary': """
        Server framework 101: A New Application"
    """,

    'description': """
        Starting module for "Server framework 101: A New Application"
    """,

    'author': "Odoo",
    'website': "https://www.odoo.com/",
    'category': 'Tutorials',
    'version': '0.1',
    'application': True,
    'installable': True,
    'depends': ['base'],

    'data': [
        "data/estate.tag.csv",
        "data/estate.property.csv",
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_menu_views.xml",
    ],
    'assets': {
    },
    'license': 'LGPL-3'
}
