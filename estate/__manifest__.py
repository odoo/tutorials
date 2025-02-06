{
    'name': "estate app",
    'summary': """
        estate app"
    """,
    'description': """
        A real estate application for selling and renting properties"
    """,
    'author': "Odoo",
    'category': 'Tutorials/estate',
    'depends': ['base'],
    'application': True,
     'data': [
        'security/ir.model.access.csv',
        'views/estate_menus.xml',
        'views/estate_property_views.xml'
    ],
    'license': 'AGPL-3'
}
