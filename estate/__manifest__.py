{   "name" : "estate",
    "version": "1.2",
    "category": "Real Estate/Brokerage",
    "description": "",
    "depends" : [ "base" ],
    "data" : [ 
        "security/security.xml",
        "security/ir.model.access.csv",
        "view/estate_pro_tag_view.xml",
        "view/estate_pro_offer_view.xml",
        "view/estate_pro_type_view.xml",
        "view/estate_property_views.xml",
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