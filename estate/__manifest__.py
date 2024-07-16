{
    'name': "estate",

    'description': """
        sell and manage your property
    """,

    'author': "Sourabh",
    'category': 'Tutorials/estate',
    'version': '0.1',
    'application': True,
    'installable': True,
    'depends': ["base"],

    'data': [
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
    'demo': [],

    'license': 'AGPL-3'
}
