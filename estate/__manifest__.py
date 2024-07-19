{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "GAJA",
    'category': 'Real Estate/Brokerage',
    'description': """
    Hell Hoo
    """,
    'data': [
        'security/security.xml',
        'data/estate.property.type.csv',
        'security/ir.model.access.csv',
        'report/estate_property_offer_template.xml',
        'report/estate_property_templates.xml',
        'report/estate_property_reports.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/res_users_views.xml',
        'views/res_config_settings_views.xml',
        'views/estate_menus.xml',
    ],
    'demo': [
        'demo/estate_demo_data_views.xml'
    ],
    "images": ["static/description/new.png"],
    'application': True,
    'license': 'AGPL-3',
}
