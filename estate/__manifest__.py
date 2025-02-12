{
    "name": "Real Estate",
    "version": "18.0",
    "author": "Odoo PS",
    "license": "LGPL-3",
    "website":"https://www.odoo.com/",
    "depends": ["base"],
    "application": True,
    "category": "Real Estate/Brokerage",
    "description": """
   Real Estate Test Description
    """,
    "data": [
        "security/ir.model.access.csv",
        "views/res_users_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_menus.xml",
        "security/security.xml",
    ],
}
