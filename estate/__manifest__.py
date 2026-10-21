{
    'name': "Estate",

    'summary': """
        Starting module for "Master the Odoo web framework, Server framework 101"
    """,

    'description': """
        Starting module for "Master the Odoo web framework, Server framework 101"
    """,

    'author': "FRCHA",
    'category': 'Tutorials',
    'version': '0.1',
    'application': True,
    'installable': True,
    'depends': ['base'],
    'data': [
        'security/ir.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menu_views.xml',
    ],
    'license': 'AGPL-3'
}
