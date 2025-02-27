{   "name" : "estate",
    "version": "1.2",
    "category": "Real Estate/Brokerage",
    "description": "",
    "depends" : [ "base", "website", "mail" ],
    "data" : [ 
        "security/security.xml",
        "security/ir.model.access.csv",
        "report/estate_property_reports.xml",
        "report/estate_property_templates.xml",
        "report/estate_property_user_report.xml",
        "report/estate_property_user_template.xml",
        "view/estate_pro_tag_view.xml",
        "view/estate_pro_offer_view.xml",
        "view/estate_pro_type_view.xml",
        "view/estate_property_views.xml",
        "view/property_list.xml",
        "view/property_list_detail.xml",
        "view/res_users_inherit.xml",
        "view/estate_model_action.xml",
        "data/master_data.xml"
    ],
    "demo" :[
        "demo/demo_property_data.xml",
        "demo/demo_offer_data.xml"
    ],
    "installable": True,
    "application": True, 
    "license": "LGPL-3"
}