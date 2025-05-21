{
    'name': "estate",

    'description': """
        Module to deal with estate sales."
    """,

    'author': "Odoo S.A.",

    "license": "LGPL-3",

    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_offer_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tags_views.xml',
        'views/estate_user.xml',
        'views/estate_menus.xml',
        'data/master_data.xml',
    ],

    'demo': [
        'demo/demo_data.xml'
    ],

    "application": True,
}
