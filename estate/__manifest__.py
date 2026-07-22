{
    'name': "Real Estate",
    'version': '1.0.0',
    'depends': ['base'],
    'author': "Amr (amgom)",
    'category': 'Real Estate',
    'description': """
    This is a real estate management module that allows users to manage properties, agents, and clients.
    """,
    'application': True,
    'data': ['security/ir.model.access.csv',
             'views/estate_property_views.xml',
             'views/estate_menus.xml'
            ],
}