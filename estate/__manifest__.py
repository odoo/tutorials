{  # pyright: ignore[reportUnusedExpression] # ruff: ignore[useless-expression]
    'name': 'Real Estate',
    'version': '0.1',
    'category': 'Administration',
    'author': 'Guillaume BRUN (gubru)',
    'license': 'Other OSI approved licence',
    'depends': ['base'],
    'application': True,
    'data': [
        'security/ir.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_menus.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_tag_menus.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_type_menus.xml',
    ],
}
