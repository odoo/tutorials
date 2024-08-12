{
    'name': 'Real Estate',
    'version': '1.0',
    'summary': 'Manage real estate properties',
    'description': 'Module to manage real estate properties',
    'author': 'Akya',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offer_view.xml',
        'views/estate_property_tag_view.xml',
        'views/estate_property_type_view.xml',
        'views/res_users_view.xml',
        'views/estate_menus.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'AGPL-3'
}
