{
    'name': 'Real Estate',
    'description': 'Real Estate Application.',
    'summary': 'Real Estate Application for beginner.',
    'depends': ['base'],
    'author': 'Aaryan Parpyani (aarp)',
    'category': 'Tutorials/RealEstate',
    'version': '1.0',
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tags_views.xml',
        'views/res_users_views.xml',
        'views/estate_property_views.xml',
        'views/estate_menus_views.xml',
    ]
}
