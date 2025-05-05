{
    "name": "Last Purchase Price in Products and Pricelists",
    "version": "1.0",
    "summary": "Shows last purchase price on product page and adds it to pricelist options.",
    "description": """
        Enhances product and pricelist functionality:
        - Adds a computed 'Last Purchase Price' field to product.template
        - Adds a 'Based on: Last Purchase Price' option in pricelist rules
    """,
    "category": "Product",
    "author": "Odon't",
    "website": "https://odoo.com",
    "depends": ["product", "purchase"],
    "data": [
        "views/product_template_views.xml",
        "views/pricelist_item_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "license": "LGPL-3",
}
