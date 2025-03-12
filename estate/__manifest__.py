{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base', 'mail', 'website'],
    'author': "Prince Beladiya",
    'category': 'Real Estate/Brokerage',
    'description': """
    The Real Estate Advertisement module
    """,
    'application': True,
    'license': 'LGPL-3',
    'data': [
        'data/estate.property.type.csv',
        'data/estate_property_menu.xml',
        'security/estate_groups.xml',
        'security/estate_security.xml',
        'security/ir.model.access.csv',
        'demo/estate_property_demo.xml',
        'demo/estate_property_offers_demo.xml',
        'report/estate_property_templates.xml',
        'report/estate_property_reports.xml',
        'wizard/offer_multi_property_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_template.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/res_config_settings_views.xml',
        'views/estate_menu_views.xml',
        'views/res_users_views.xml'
    ]
}
