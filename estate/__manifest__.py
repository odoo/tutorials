{
    'name': "Real Estate App",
    'version': '1.0',
    'depends': ['base', 'website', 'sale_management', 'sale'],
    'author': "KSKU",
    'category': 'Real Estate/Brokerage',
    'description': """
    First odoo app
    """,
    # data files always loaded at installation
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'report/estate_property_offer_templates.xml',
        'report/estate_property_templates.xml',
        'report/estate_property_users_templates.xml',
        'report/estate_property_reports.xml',
        'wizard/offer_automatic_made_wizard_views.xml',
        'views/estate_sale_order_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/res_users_views.xml',
        'views/res_config_settings_views.xml',
        'views/estate_sales_menus.xml',
        'views/estate_menus.xml',
        'views/property_detail_template.xml',
        'views/property_list_template.xml',
        'views/website_menus.xml',
        'data/estate.property.type.csv',
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
        'demo/estate_property_demo.xml',
    ],
    'images': [
        "static/description/realstate.png",
        "static/description/abcd.png",
        "static/description/dcba.jpeg"],
    'installable': True,
    'application': True,
    'license': 'AGPL-3',
}
