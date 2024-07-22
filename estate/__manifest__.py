{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base', 'website'],
    'author': "Ashutosh Yadav",
    'category': 'Real Estate/Brokerage',
    'description': """
    Description text
    """,
    # data files always loaded at installation
    'data': [
        'data/template/estate.property.type.csv',
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'report/estate_property_offer_templates.xml',
        'report/estate_property_users_templates.xml',
        'report/estate_property_templates.xml',
        'report/estate_property_reports.xml',
        'views/res_users_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_templates.xml',
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
