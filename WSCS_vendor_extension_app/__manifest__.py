{
    "name": "WSCS_vendor_extension_app",
    "author": "Bhavya Nanavati",
    "depends": ["purchase", "stock", "WSCS_product_extension_app"],
    "data": [
        "security/ir.model.access.csv",
        "views/view_partner_form_inherit.xml",
        "views/vendor_status_views.xml",
        "views/vendor_pricelist_inherit.xml",
        "views/gfsi_certification_views.xml",
        "views/gfsi_grade_views.xml",
        "views/gfsi_scheme_views.xml",
        "views/menuitems.xml",
        "data/vendor_data.xml",
        "data/vendor_status_data.xml",
    ],
    "auto_install": True,
    "license": "LGPL-3",
}
