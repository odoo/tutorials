{
    "name": "Estate",
    "license": "LGPL-3",
    "application": True,
    "depends": ["base",'mail','website'],
    'category': 'Real Estate/Brokerage',
    "description": """ 
    The Real Estate Advertisement module.
    """,
    "data": [
        "security/estate_security.xml",
        "security/ir.model.access.csv",
        "report/estate_property_templates.xml",
        "report/estate_property_report.xml",
        "views/estate_property_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_menus.xml",
        "views/res_users_views.xml",
        "views/estate_website_template.xml",
        "views/res_config_settings.xml",
        "wizard/estate_property_wizard_view.xml",  
        "data/estate_property_menu.xml",      
    ],
    "demo": ["demo/estate_property_demo.xml",
            "demo/estate_property_offers.xml",
    ],
}
