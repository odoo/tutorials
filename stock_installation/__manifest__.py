{
    'name': "Stock Transport Installation Settings",
    'version': '1.0',
    'depends': ['stock'],
    'author': "Ayushmaan Ayve",
    'category': 'Stock Transport Installation Settings',
    'description': """
        Stock Transport Installation Settings
    """,
    # data files always loaded at installation
    'data': [
        'views/res_config_settings_view.xml',
    ],
    'demo': [],
    'application': False,
    'installable': True,
    'auto_install': True,
}