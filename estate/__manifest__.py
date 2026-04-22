{
    'name': "Estate",
    'summary': """
        The Real Estate Advertisement module
    """,

    'description': """
        The Real Estate Advertisement module
    """,
    'author': "Odoo",
    'website': "https://www.odoo.com/",
    'category': 'Tutorials',
    'version': '0.1',
    'application': True,
    'installable': True,
    'depends': ['base'],
    'data': [
        'data/ir.model.access.csv',
        'views/estate_property_views.xml',
        'data/estate_menus.xml',
    ],
    'license': 'AGPL-3'
}