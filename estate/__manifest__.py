{
    'name': "estate",

    'description': """
        sell and manage your property
    """,

    'author': "Sourabh",
    'category': 'Real Estate/Brokerage',
    'version': '0.1',
    'application': True,
    'installable': True,
    'depends': ["base"],

    'data': [
        'security/estate_security.xml',
        'data/estate.property.type.csv',
        'security/ir.model.access.csv',
        'views/res_config_settings_view.xml',
        'views/estate_property_tag_view.xml',
        'views/estate_property_offer_view.xml',
        'views/res_users_view.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_menus.xml',
    ],
    "images": ["static/description/icon.png"],
    'demo': [
        'demo/demo_data.xml',
    ],

    'license': 'AGPL-3'
}
