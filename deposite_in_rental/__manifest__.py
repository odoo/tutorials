{
    "name": "deposite_in_rental",
    "depends": ["base", "account_invoice_extract", "sale_renting", "website_sale"],
    "data": [
        "views/res_config_setting_rental_view.xml",
        "views/product_template_inherit_view.xml",
        "views/website_rental_inherit.xml",
        "views/sale_order_line_inherit_view.xml",
    ],
    "license": "LGPL-3",
}
