{
    'name': "Estate",
    'summary': """
        App module created specifically for the Server Framework 101 tutorial. 
    """,
    'description': """
        App module created specifically for the Server Framework 101 tutorial.
    """,
    'author': "Odoo",
    'website': "https://www.odoo.com",
    'category': 'Tutorials',
    'version': '0.1',
    'depends': ['base', 'web'],
    'application': True,
    'installable': True,
    'data': [
        'data/ir.model.access.csv',
        'views/templates.xml',
    ],
}