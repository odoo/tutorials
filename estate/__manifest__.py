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
    'images': ['static/description/thumbnail.png'],
    'data': [
        'data/templates/estate.property.type.csv',
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/res_users_views.xml',
        'views/res_config_settings_views.xml',
        'views/estate_menus.xml',
    ],
    'demo': [
        'demo/demo_data.xml',
    ],
    'license': 'AGPL-3',
}
