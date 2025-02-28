{
    "name": "webshop_extension",
    "description": """
    This module add an extended description field in the website ecommerce application.
        - added multilingual HTML description field in product template
        - displays this field in the frontend
        - enable import/export of this field
    """,
    "summary": "Adds extended description field in the website ecommerce application",
    "author": "Vedant Pandey (vpan)",
    "version": "1.0",
    "category": "website",
    "data": [
        "views/product_views.xml",
        "views/product_web_template.xml"
    ],
    "depends": ["website_sale"],
    "installable": True,
    "license": "LGPL-3"
}
