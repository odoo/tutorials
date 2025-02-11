{
    "name": "Real Estate",
    "version": "1.0",
    "author": "hsha",
    "license": "LGPL-3",
    "depends": ["base"],
    "application": True,
    "description": """
   Real Estate Test Description
    """,
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_menu.xml",
    ],
    'installable': True,
}
