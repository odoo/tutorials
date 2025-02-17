{
    'name': 'Estate',
    'author': 'Odoo - Utsav',
    'license': 'LGPL-3',
    'category': 'Real Estate/Brokerage',
    'depends':['base'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/res_users_view.xml',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menus.xml',
    ],
    'application': True,
    'auto_install': False,
}
