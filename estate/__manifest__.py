{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "djsh",
    'sequence':1,
    'category': 'Category',
    'description': """
    Real Estate Properties With all the information
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ],
    # data files containing optionally loaded demonstration data
    # 'demo': [
    #     'demo/demo_data.xml',
    # ],
    'application': True,

}
