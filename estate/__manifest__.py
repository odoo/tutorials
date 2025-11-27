{
    'name': "Real Estate",
    'summary': "Testing the real estate module",
    'description': "Testing the description real estate module",
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_users_views.xml',
        'views/estate_property_offer_view.xml',
        'views/estate_property_view.xml',
        'views/estate_property_type_view.xml',
        'views/estate_property_tag_view.xml',
        'views/estate_menus.xml',
    ],
    'application': True,
    'author': "Odoo",
    'license': 'LGPL-3',
}
