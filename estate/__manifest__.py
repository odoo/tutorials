{  # pyright: ignore[reportUnusedExpression] # ruff: ignore[useless-expression]
    'name': 'Real Estate',
    'depends': ['base'],
    'application': True,
    'data': [
        'security/ir.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_menus.xml',
    ],
}
