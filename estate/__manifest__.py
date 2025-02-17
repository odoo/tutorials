{
    "name": "estate app",
    "summary": "Estate module",
    "author": "Odoo",
    "category": "Real Estate/Brokerage",
    "version": "1.0",
    "depends": ["base","mail"],
    "application": True,
    "installable": True,
    "data": [
      "security/estate_security.xml",
      "security/ir.model.access.csv",
      "data/mail_message_subtype.xml",
      "data/estate.property.type.csv",
      "views/estate_property_offer_views.xml",
      "views/estate_property_types_views.xml",
      "views/estate_users_view.xml",
      "views/estate_property_tag_views.xml",
      "views/estate_property_views.xml",
      "views/estate_menus.xml",
    ],
    "demo": [
      "demo/demo_data.xml",
    ],
    "license": "AGPL-3"
}
