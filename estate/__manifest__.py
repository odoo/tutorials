{
    "name": "Estate Management",
    "version": "1.0",
    "category": "Real Estate",
    "summary": "Manage Estate Properties, Leases, and More",
    "description": """
        This module allows you to manage properties, sales, rentals, and other real estate-related data in your Odoo system.
    """,
    "author": "Your Name or Company",
    "website": "https://www.yourcompanywebsite.com",
    "depends": ["base"],  # Specify any dependencies here
    "license": "LGPL-3",
    "data": [
        # Views and menus
        "views/estate_property_offer_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_views.xml",  # Views for estate properties
        "views/res_users_views.xml",
        "views/estate_menus.xml",  # Menus for estate properties
        # Security files
        "security/ir.model.access.csv",  # Access control file for models
    ],
    "demo": [
        # Optional: List demo data files if any
        # 'demo/estate_demo_data.xml',
    ],
    "images": ["static/description/icon.png"],
    "installable": True,  # Whether this module can be installed
    "application": True,  # Whether this module is an application (will show on the main screen)
    "auto_install": False,  # Whether the module should auto-install when dependencies are met
}
