{
    'name': "estate",

    'description': """
        Module to deal with estate sales."
    """,

    'author': 'Odoo S.A.',

    'license': 'LGPL-3',

    'category': 'Real Estate/Brokerage',

    'data': [
        'views/estate_property_offer_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tags_views.xml',
        'views/estate_user.xml',
        'views/estate_menus.xml',
        'data/master_data.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
    ],

    'demo': [
        'demo/demo_data.xml'
    ],

    'application': True,
}
