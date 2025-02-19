{
    "name": "Real Estate",
    "version": "0.1",
    "category": "Administration",
    "sequence": 100,
    "license": "LGPL-3",
    "author": "Odoo S.A.",
    "summary": "Track real estate",
    "description": "",
    "website": "https://www.odoo.com/page/estate",
    "depends": [
        "base",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_menus.xml",
        "views/res_users_view.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
