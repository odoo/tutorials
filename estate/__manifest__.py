{
    'name': 'Real Estate',
    'version': '1.0',
    'description': 'Manage real estate properties',
    'summary': 'A basic Real Estate module',
    'author': 'Abhishek Khant (abhk)',
    'depends': ['base', 'sale'],
    'category': 'Sales',
    'data': [
        'security/ir.model.access.csv',
        'views/property/estate_property_views.xml',
        'views/property/estate_property_type_views.xml',
        'views/estate_property_actions.xml',
        'views/estate_property_menu.xml',
    ],
    'application': True,
    'installable': True
}
