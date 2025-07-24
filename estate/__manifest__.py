{
    'name': "estate",
    'version': '1.0',
    'category': 'Sales/RealEstate',
    'summary': 'Track and deal with real estate properties.',
    'author': "Odoo S.A.",
    'description': """
    Description text
    """,
    'depends': ['base'],
    'installable': True,
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/res_users_views.xml',
        'views/estate_menus.xml',
    ],
    'license': 'LGPL-3',
}
