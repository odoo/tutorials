{
    "name": "Estate",
    "version": "1.0",
    "category": "Real Estate/Brokerage",
    'depends': ['base','mail'],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/estate_property_offer_view.xml",
        "views/estate_property_view.xml",
        "views/estate_property_type_view.xml",
        "views/estate_property_tag_view.xml",
        "views/res_users_view.xml",
        "views/estate_menus.xml",
        "data/master_data.xml",
        "report/estate_property_templates.xml",
        "report/estate_property_reports.xml",
        "report/res_users_reports.xml",
        "report/res_users_templates.xml",
    ],
    "demo":[
        "demo/estate_property_demo_data.xml",
    ],
    "installable": True,
    "application": True,
}

