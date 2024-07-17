{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "Ashutosh Yadav",
    'category': 'Real Estate',
    'description': """
    Description text
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'data/template/estate.property.type.csv',
        'views/res_users.xml',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menus.xml',
        'views/res_config_settings_views.xml'
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
        'demo/estate_demo.xml',
    ],
    "image": ["static/descriptions/selfie.png"],
    'installable': True,
    'application': True,
    'license': 'AGPL-3'
}
