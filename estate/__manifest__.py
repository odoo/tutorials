{
    "name": "Real Estate",
    "version": "1.0",
    "category": "Tutorial",
    "summary": "Manage real estate properties",
    "author": "sasri-odoo",
    "license": "LGPL-3",
    "depends": ["base", 'mail'],
    "data": [
        "security/estate_security.xml",
        "security/ir.model.access.csv",
        "views/estate_property_visit_views.xml",
        "views/estate_property_maintenance.xml",
        "views/estate_property_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_menus.xml",
        "views/estate_res_user_views.xml",
        "demo/estate_property_data.xml",
        "data/mail_template_data.xml"
    ],
    "application": True,
}
