{
    "name": "Supplier Portal",
    "summary": """
        Supplier portal for uploading 
    """,
    "description": """
        Supplier portal for uploading documents
    """,
    "author": "Odoo",
    "website": "https://www.odoo.com",
    "category": "Tutorials/Supplier_Portal",
    "version": "1.0",
    "installable": True,
    "auto_install": True,
    "depends": ["base_setup", "website", "account"],
    "data": ["views/supplier_portal_template.xml","views/supplier_website.xml"],
    "license": "AGPL-3",
}
