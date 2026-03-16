{
    'name': "Real State",
    'version': '1.0',
    'depends': ['base'],
    'author': "kiro",
    'category': 'Category',
    'description': """
    Description text
    """,
    # data files always loaded at installation
    'data': [
        'views/mymodule_view.xml',
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
        'demo/demo_data.xml',
    ],
    'application': True,
    'category': 'Tutorials',
    'installable': True
}