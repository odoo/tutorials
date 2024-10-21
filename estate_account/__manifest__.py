{
    'name': "Estate Accounting",
    'version': '1.0',
    'depends': ['base', 'account'],
    'author': "Odoo S.A.",
    'license': "LGPL-3",
    'category': 'Estate/Accounting',
    'application': False,
    'auto_install': True,
    'description': """
    Tutorial app - Accounting extension for Estate model
    """,
    # data files always loaded at installation
    'data': [
        'views/estate_account_menus_view.xml',
        'views/estate_account_menus_view.xml',
        'views/estate_property_view.xml',
        'views/account_move_view.xml',
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
    ],
}
