{
    'name': "Real Estate",
    'version': '18.0',
    'depends': ['base'],
    'author': "matd",
    'category': 'Category',
    'sequence' : 1,
    'description': """
    It's provide real estate module
    """,
    'application': True,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ],

    # # data files containing optionally loaded demonstration data
    # 'demo': [
    #     'demo/demo_data.xml',
    # ],
}