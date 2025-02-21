{
    "name": "estate app",
    "summary": "Estate module",
    "author": "Odoo",
    "category": "Real Estate/Brokerage",
    "version": "1.0",
    "depends": ["base","website","web","mail"],
    "application": True,
    "installable": True,
    "data": [
      "security/estate_security.xml",
      "security/ir.model.access.csv",
      "data/mail_message_subtype.xml",
      "data/estate.property.type.csv",
      "views/estate_template.xml",
      "views/estate_property_offer_views.xml",
      "views/estate_property_types_views.xml",
      "views/res_users_view.xml",
      "views/estate_property_tag_views.xml",
      "views/estate_property_views.xml",
      "views/estate_menus.xml",
      "report/estate_property_reports.xml",
      "report/estate_property_template.xml",
      "report/res_users_property_template.xml",
      "report/estate_property_offers_template.xml"
    ],
    "demo": [
      "demo/demo_data.xml",
    ],
    "license": "AGPL-3"
}
