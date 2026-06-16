{
    "name": "Supplier Portal",
    "application": False,
    "installable": True,
    "author": "sngoh",
    "depends": ["base", "website", "account"],
    "auto_install": True,
    "license": "LGPL-3",
    "data": [
        "views/portal_templates.xml",
        "views/account_supplier_portal_view.xml",
    ],
}
