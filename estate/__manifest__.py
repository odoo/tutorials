{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "Odoo",
    'category': 'Real Estate/Brokerage',
    'summary': """
        Real Estate Summary
    """,
    'description': """
        Description text
    """,
    # data files always loaded at installation
    'data': [
        "security/security.xml",
        'security/ir.model.access.csv',
        'report/estate_property_templates.xml',
        'report/estate_property_reports.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_views.xml',
        'views/res_users_views.xml',
        'views/estate_menus.xml',
        'views/res_config_settings_views.xml',
    ],
    # # data files containing optionally loaded demonstration data
    'demo': [
        'data/template/estate.property.type.csv',
        'demo/estate.property.xml',
    ],
    'license': 'AGPL-3',
    'application': True
}
