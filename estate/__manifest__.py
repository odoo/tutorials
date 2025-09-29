{
    'name': "Real Estate",
    'author': "Odoo",
    'website': "https://www.odoo.com/",
    'category': 'Real Estate',
    'version': '0.1',
    'application': True,
    'depends': ['base'],
    'license': 'AGPL-3',
    'data': [
        'views/estate_property_offer_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'security/estate_security.xml',
        'views/estate_menus.xml',
        'views/res_users_view.xml',
        'security/ir.model.access.csv',
    ]
}
