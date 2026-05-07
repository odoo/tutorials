{
    'name': "Estate",
    'version': '1.0',
    'depends': ['base', 'mail'],
    'author': "Asurk",
    'category': 'Real Estate/Brokerage',
    'description': """
    A module so that customers can bid on real estates
    """,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tags_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_visit_views.xml',
        'views/estate_menus.xml',
        'views/res_users_views.xml'
    ],
    'license': 'LGPL-3',  # Default License
    'application': True,
    'installable': True,
    # data files always loaded at installation

}
