{
    'name': 'Real Estate',
    'version': '0.0',
    'category': 'Sale/estate',
    'summary': 'Manage your Real Estate Assets',
    'license': 'LGPL-3',
    'application': True,
    'installable': True,
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_type_offer.xml',
        'views/estate_property_type_views.xml',
        'views/estate_user_views.xml',
        'views/estate_menus.xml',
    ],
}
