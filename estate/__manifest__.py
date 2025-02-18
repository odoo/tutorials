{
    "name": "Real Estate",
    "version": "1.0",
    "category": "Real Estate/Brokerage",
    "depends": ["base", "mail"],
    "data": [
        "report/salesperson_property_template.xml",
        "report/estate_property_offers_template.xml",
        "report/estate_property_template.xml",
        "report/estate_report_action.xml",
        "security/security.xml",
        "security/ir.model.access.csv",
        "wizard/estate_property_offer_wizard_view.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_listing_template.xml",
        "views/estate_property_views.xml",
        "views/res_users_inherited_views.xml",
        "views/estate_menus.xml",
        "data/estate.property.type.csv"
    ],
    "demo": [
        "demo/estate_property_demo.xml"
    ],
    "installable": True,
    "application": True
}
