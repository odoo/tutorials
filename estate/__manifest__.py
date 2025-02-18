{
    "name": "Real Estate",
    "version": "1.0",
    "depends": ["mail","website"],
    "author": "odoo",
    "license": "LGPL-3",
    "description": """
This is Real Estate application which makes easy to sold property
    """,
    "application": True,
    "data": [
        "security/estate_security.xml",
        "security/ir.model.access.csv",
        "data/estate_data.xml",
        "report/estate_property_templates.xml",
        "report/estate_property_reports.xml",
        "views/estate_templates.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_users_views.xml",
        "views/estate_property_menus.xml",
    ],
    "demo": [
        "data/estate_property_demo.xml",
        "data/estate_property_offer_demo.xml"
    ],
}
