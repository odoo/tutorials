{
    'name': "real-estate",
    'version': "1.0",
    'depends': ["base"],
    'author': "Dhruv",
    'category': "Tutorials/estate",
    'application': True,
    'installable': True,
    'description': """
    Module for the practice and getting knowledge in the technicality
    """,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/res_users_views.xml',
        'views/estate_menus.xml',
    ],
    'demo': [],
    'license': 'AGPL-3',
}
