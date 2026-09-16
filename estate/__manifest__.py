# __manifest__.py
{  # noqa: B018
    "author": "mawat",
    "name": "estate",
    "depends": ["base"],
    "application": True,
    "license": "LGPL-3",
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_menus.xml"
    ],
}
