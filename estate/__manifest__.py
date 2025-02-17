{
    "name": "Estate",
    "description": "Real Estate Module",
    "version": "1.0",
    "depends": ["base",'mail'],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "report/public_property_templates.xml",
        "report/public_property_report.xml",
        "views/res_users.xml",
        "views/public_property_views.xml",
        "views/estate_menus.xml",
        "data/public.property.type.csv",
    ],
    "demo":[
        "demo/public_property_demo.xml"
    ],
    "application": True,
    "author": "Lucky Prajapati (prlu)",
    "category": "Real Estate/Brokerage",
    "license": "LGPL-3",
}
