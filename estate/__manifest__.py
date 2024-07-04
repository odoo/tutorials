{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "Ashutosh Yadav",
    'category': 'Real Estate',
    'description': """
    Description text
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml'
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
    ],
    'application': 'true',
    'license': 'AGPL-3'
}
