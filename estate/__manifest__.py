{
    'name': "Real Estate App",
    'version': '1.0',
    'depends': ['base'],
    'author': "KSKU",
    'category': 'Category',
    'description': """
    First odoo app
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/res_users_views.xml',
        'views/estate_menus.xml',
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
    ],
    'installable': True,
    'application': True,
    'license': 'AGPL-3',
}
