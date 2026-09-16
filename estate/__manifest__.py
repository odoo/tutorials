{
    'name': "Estate",
    'author': "Arthur De Clerck",
    'license': "LGPL-3",
    'depends': ['base'],
    'category': "Real Estate/Brokerage",
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        # 'security/security.xml',

        'views/estate_menus.xml',
        'views/estate_property_views.xml',
    ]
}