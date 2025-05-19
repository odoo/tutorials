{
    'name': 'Real estate',
    'version': '0.1',
    'depends': ['base'],
    'author': 'odoo SA',
    'category': 'Finance',
    'description': """
    Empty real estate app for tutorial purposes
    """,
    'application': 'True',
    'data': [
        'security/ir.model.access.csv',
        'view/estate_property_views.xml',
        'view/estate_menus.xml',
    ],
    'license': 'LGPL-3',
}
