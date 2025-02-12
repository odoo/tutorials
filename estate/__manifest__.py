{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "Odoo PS",
    'website': 'https://www.odoo.com/',
    'license': 'LGPL-3',
    'category': 'Category',
    'description': "this is description",
    'application': True,
    'installable': True,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_res_users_views.xml',
        'views/estate_menus.xml',
    ],
    'demo': [
    ],
}
