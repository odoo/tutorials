{
    "name": "Estate",
    "version": "19.0.1.0.0",
    "depends": [
        "base",
        ],
    "author": "Roman (rohar)",
    "description": """
    Real Estate Advertisement
    """,
    # data files always loaded at installation
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_menus.xml",
        "views/res_user_views.xml",
    ],
    # data files containing optionally loaded demonstration data
    "demo": [],
    "application": True,
    "license": "LGPL-3",
}
