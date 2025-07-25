{
    "name": "Real Estate",
    "category": "Tutorials/RealEstate",
    "version": "1.0",
    "summary": "Real Estate module",
    "depends": [
        "base",
    ],
    "data": [
        # "security/crm_security.xml",
        "security/ir.model.access.csv",
        "views/res_users_views.xml",
        "views/estate_property_views.xml",
        "views/estate_offer_views.xml",
        "views/estate_type_views.xml",
        "views/estate_tag_views.xml",
        "views/estate_menus.xml",
    ],
    "installable": True,
    "application": True,
    "license": "AGPL-3",
}
