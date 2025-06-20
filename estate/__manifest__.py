{
    'name': "estate",
    'version': '18.0.1.0.0',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_type_views.xml',
        'views/res_users_views.xml',
        'views/estate_menus.xml',
        ],
    'author': "baje",
    'category': 'Uncategorized',
    'description': """
    An app to manage a Real Estate Agency
    """,
    'application': True,
    'license': 'LGPL-3',
}
