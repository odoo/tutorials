{
    'name': 'Real Estate',
    'version': '1.0',
    'summary': 'A basic Real Estate module',
    'description': 'Manage real estate properties',
    'author': 'Abhishek Khant (abhk)',
    'depends': ['base', 'sale'],
    'category': 'Sales',
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/inherited_user_views.xml',
        'views/estate_property_menu.xml'
    ],
    'application': True,
    'installable': True,
    'license': 'LGPL-3'
}