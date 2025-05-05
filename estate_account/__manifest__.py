{
    "name": "Estate Accounting",
    "version": "1.0",
    "category": "Real Estate",
    "summary": "Integrates Estate Properties with Accounting",
    "description": """
        This module links the Estate Management module with Odoo Accounting.
        It will later support invoice generation and financial tracking for property sales.
    """,
    "author": "Your Name or Company",
    "website": "https://www.yourcompanywebsite.com",
    "depends": ["estate", "account"],  # Depends on both estate and account modules
    "license": "LGPL-3",
    "data": [
        # No views or menus yet
    ],
    "demo": [
        # Optional: List demo data files if any
        # 'demo/estate_account_demo.xml',
    ],
    "images": ["static/description/icon.jpg"],  # Add your icon if desired
    "installable": True,
    "application": True,
    "auto_install": False,
}
