{
    "name": "estate app",
    "description": """
        A real estate application for selling and renting properties
    """,
    "author": "Odoo",
    "category": "Real Estate/Brokerage",
    "depends": ["base", "mail" , "website"],
    "application": True,
    "data": [
        "security/estate_security.xml",
        "security/ir.model.access.csv",
        "data/estate.property.type.csv",
        "data/estate_property_status_subtypes.xml",
        "report/estate_property_report.xml",
        "report/estate_property_template.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/res_users.xml",
        "views/estate_property_views.xml",
        "views/estate_website_template.xml",
        "views/estate_menus.xml",
    ],
    "demo": [
        "demo/demo_data.xml",
    ],
    "license": "AGPL-3",
}
