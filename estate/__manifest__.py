{
    "name": "estate app",
    "summary": "Estate module",
    "author": "Odoo",
    "category": "Tutorials/estate",
    "version": "1.0",
    "depends": ["base"],
    "application": True,
    "installable": True,
    "data": [
      "security/security.xml",
      "security/ir.model.access.csv",
      
      "views/estate_users_view.xml",
      "views/estate_property_offer.xml",
      "views/estate_property_tag.xml",
      "views/estate_property_views.xml",
      "views/estate_property_types.xml",
      "views/estate_menus.xml",
    ],
    "license": "AGPL-3"
}
