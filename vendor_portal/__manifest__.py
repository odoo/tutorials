{
    "name": "vendor_portal",
    "version": "1.0",
    "description": "Vendor",
    "summary": "",
    "author": "Odoo",
    "website": "www.odoo.com",
    "license": "LGPL-3",
    "depends": ["purchase", "stock", "website_sale"],
    "data": [
        "views/vendor_portal_template.xml",
        "data/website_menu_data.xml",
    ],
    "application": True,
    "installable": True,
}
