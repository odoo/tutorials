{
    "name": "Real Estate",
    "version": "1.0",
    "author": "drat-odoo",
    'depends': ['base','website'],
    "sequence": "20",
    "category": "Real Estate/Brokerage",
    "description": """
This is test version of estate (for learning purpose).
    """,
    "data": [
        "security/estate_security.xml",
        "security/ir.model.access.csv",
        "views/estate_property_offer_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_views.xml",
        "views/res_users_views.xml",
        "views/estate_menus.xml",
        "data/estate.property.type.csv",
        "report/estate_property_reports.xml",
        "report/estate_property_reports_templates.xml",
        "views/estate_website_menu.xml",
        "views/estate_property_list_template.xml",
        "views/estate_property_details_template.xml",
    ],
    "demo": [
        "demo/estate_property_demo.xml",
    ],
    "installable": True,
    "application": True,
    "license": "OEEL-1",
}
