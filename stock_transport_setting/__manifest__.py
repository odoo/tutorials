{
    'name': "Stock Transport Settings",
    'version': '1.0',
    'depends': ['stock_picking_batch'],
    'author': "Harsh Chaudhari",
    'category': 'Stock Transport Settings',
    'description': """
    Stock Transport Settings description...
    """,
    # data files always loaded at installation
    'data': [
        'views/res_config_settings_views.xml',
    ],
    # data files containing optionally loaded demonstration data
    'demo': [],
    'application': False,
    'installable': True,
    'auto_install': True,
}
