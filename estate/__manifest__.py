{
    'name': 'Real Estate',
    'description': "Real Estate Management",
    'depends': [
        'base'
    ],
    'author': "sbbh",
    'category': 'Real Estate/Brokerage',
    'data': [
        'security/ir.model.access.csv',
        
        'views/estate_property_views.xml',
        'views/estate_property_type.xml',
        'views/estate_property_tag.xml',
        'views/estate_property_offer.xml',
        'views/res_users_view.xml',
        'views/estate_menus.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
