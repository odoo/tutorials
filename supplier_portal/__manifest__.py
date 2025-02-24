{
    "name": "Supplier Portal",
    "summary": "Allow suppliers to upload invoices (PDF & XML) via a portal and create draft bills.",
    "description": """
    This module provides a dedicated supplier portal where suppliers can log in and upload their invoices in PDF and XML format. Upon submission, the system automatically creates a draft vendor bill (`account.move`) in Odoo with the uploaded files attached.
    """,
    "depends": ["website", "account"],
    "data": ["views/supplier_portal_website_template.xml"],
    "auto_install": True,
    "license": "LGPL-3",
}
