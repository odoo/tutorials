{
    'name': 'estate',
    'version': '1.0.0',
    'author': 'rodh',
    'category': 'Real Estate',
    'summary': 'Manage real estate properties and transactions',
    'depends': [
        'base',
    ],
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
    'data': [
    'security/ir.model.access.csv',
    'view/estate_property_views.xml',
    'view/estate_property_offer_views.xml',
    'view/estate_property_type_views.xml',
    'view/estate_property_tag_views.xml',
    'view/estate_menus.xml',
    'view/estate_res_users_view.xml'
    ],
}
