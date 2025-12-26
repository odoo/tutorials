{
    'name': "Estate",
    'summary': """
        App module created specifically for the Server Framework 101 tutorial.
    """,
    'description': """
        App module created specifically for the Server Framework 101 tutorial.
    """,
    'author': "Odoo ALMAG",
    'website': "https://www.odoo.com",
    'category': 'Tutorials',
    'depends': ['base', 'web'],
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_views.xml',
        'views/res_users_views.xml',
        'views/estate_menus.xml',
    ],
    'license': 'LGPL-3'
}
