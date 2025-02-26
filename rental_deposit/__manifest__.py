{
    "name": "Rental Deposit",
    "version": "1.0",
    "summary": "provide deposit functionality",
    "description": """
        It allow to use deposit on products and add it on sale order
    """,
    "author": "Odoo",
    "auto_install": True,
    "data": [
        "views/product_template_views.xml",
        "views/res_config_settings_views.xml",
    ],
    "license": "LGPL-3",
    "depends": ["sale_renting","sale"],
}
