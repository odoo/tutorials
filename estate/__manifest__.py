
{
    "name": "Real Estate",
    "version": "19.0.0.1.0",
    "category": "Custom",
    "summary": "My first application",
    "installable": True,
    "application": True,
    "author": "belam",
    "depends": [
        "base",
     ],
    "license": "LGPL-3",
    "data": [
        # Views per model
        "views/estate_property_offer_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_salesman_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_views.xml",
        # Menus
        "views/estate_property_menus.xml",
        # Security
        "security/ir.model.access.csv",
        # Dqtq
    ],
}
