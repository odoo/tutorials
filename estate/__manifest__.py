{
    "name": "Real Estate",
    "depends": ["base", "mail", "website"],
    "application": True,
    "author": "Parth Pujara",
    "category": "Real Estate/Brokerage",
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_property_type_menu.xml",
        "views/estate_property_tag_menu.xml",
        "views/estate_menus.xml",
        "views/estate_property_res_user_views.xml",
        "views/estate_property_website_template.xml",
        "report/estate_property_templates.xml",
        "report/estate_property_reports.xml",
    ],
    "demo":[
        "demo/estate_property_demo.xml",
        "demo/estate.property.type.csv",
    ],
    "license": "LGPL-3",
}
