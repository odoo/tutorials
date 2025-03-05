{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "Rishav Shah (sris)",
    'category': 'Estate',
    'description': """    START-UP 1    """,
    'installable':True,
    'application':True,
    'auto_install': True,
    'license':'LGPL-3',
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