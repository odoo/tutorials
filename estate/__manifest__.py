{
    'name': "Real Estate App",
    'version': '1.0',
    'depends': ['base'],
    'author': "KSKU",
    'category': 'Real Estate/Brokerage',
    'description': """
    First odoo app
    """,
    # data files always loaded at installation
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/res_users_views.xml',
        'views/res_config_settings_views.xml',
        'views/estate_menus.xml',
        'data/estate.property.type.csv'
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
        'demo/estate_property_demo.xml',
    ],
    'images': ["static/description/realstate.png"],
    'installable': True,
    'application': True,
    'license': 'AGPL-3',
}
