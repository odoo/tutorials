{
    "name": "Supplier Portal",
    "description": """
  Help supplier to provide their Invoice
    """,
    "category": "Vendor",
    "version": "1.0",
    "depends": ["account", "website"],
    "data": [
        "security/supplier_group.xml",
        "views/supplier_template.xml",
        "views/website_menu.xml",
    ],
    "auto-install": True,
    "application": False,
    "license": "LGPL-3",
}
