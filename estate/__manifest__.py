{
    'name': 'Real Estate',
    'description': 'Welcome to my Real Estate',
    'author': 'KRPAT',
    'website': 'https://www.odoo.com/',
    'category': 'Tutorials',
    'version': '1.0',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_offer_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menus.xml',
        'views/res_users_views.xml',
    ],
}
