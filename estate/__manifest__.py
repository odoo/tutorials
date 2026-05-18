{
    'name': "Estate",
    'version': '1.0',
    'depends': ['base', 'calendar'],
    'author': "habar",
    'category': 'Tutorials',
    'description': """
    This is the sample module for practise.
    """,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_visit.xml',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menus.xml',
        'views/res_users_views.xml'
    ],
    'application': True,
    'license': 'LGPL-3',
    'installable': True,
}
