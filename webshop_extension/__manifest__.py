{
    "name": "webshop_extension",
    "description": "This module adds an extended description field in the website's product view.",
    "author": "Mahavir Patel (pmah)",
    "version": "1.0",
    "category": "website",
    "depends": ["product","website_sale"],
    "data" : [
        "views/product_views.xml",
        "views/product_web_template.xml"
    ],
    'post_init_hook': 'post_init_hook',
    "installable": True,
    "license": "LGPL-3"
}
