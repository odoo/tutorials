{
    'name': 'Real Estate',
    'version': '1.0',
    'category': 'Real Estate',
    'summary': 'Module for managing real estate properties.',
    'author': 'Your Name',
    'depends': ['base'],
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'view/estate_property_views.xml',
        'view/estate_property_type_view.xml',
        'view/estate_property_tag_view.xml',
        'view/estate_property_offer_view.xml',
        'view/res_users_view.xml',
        'view/estate_menus.xml'
    ],
    'installable': True,
    'application': True,
}
