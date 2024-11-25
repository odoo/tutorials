{
    "version": "1.0",
    "name": "Real Estate",
    "category": "Real Estate/Brokerage",
    "depends": ["base"],
    "author": "djip-odoo",
    "description": """
        part of technical training
    """,
    "data": [
        # security
        "security/security.xml",
        "security/ir.model.access.csv",
        # reports
        "report/paperformat.xml",
        "report/company_details_templates.xml",
        "report/estate_property_offers_templates.xml",
        "report/res_users_reports.xml",
        "report/res_users_templates.xml",
        "report/estate_property_reports.xml",
        "report/estate_property_templates.xml",
        # views
        "views/actions_menu_and_button.xml",
        "views/menu_views.xml",
        "views/estate_property_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_offer_views.xml",
        "views/res_users_views.xml",
    ],
    "demo": [
        "demo/demo_res_company.xml",
        "demo/demo_res_users.xml",
        "demo/estate.property.types.csv",
        "demo/estate.property.tags.csv",
        "demo/estate_property_demo.xml",
        "demo/estate_property_offers_demo.xml",
    ],
    "application": True,
    "installable": True,
    "auto_install": False,
    "license": "LGPL-3",
}
