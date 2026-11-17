{
    'name': "real estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "elsa ringling (elrin)",
    'category': 'Services',
    'description': """
    This is a test module for the server framework 101 tutorial
    """,
    # data files always loaded at installation
    'data': [
        'views/mymodule_view.xml',
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
        'demo/demo_data.xml',
    ],
    'installable': True,
    'application': True
}
