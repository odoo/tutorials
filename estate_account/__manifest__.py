{
    'name': "Estate Account",
    'version': '1.0',
    'depends': ['base', 'estate', 'account', 'website'],
    'author': "GAJA",
    'category': 'Category',
    'description': """
    Hell Hoo
    """,
    # data files always loaded at installation
    'data': [
        'report/estate_property_report_inherit.xml',
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
    ],
    'application': True,
    'license': 'AGPL-3',
}
