# -*- coding: utf-8 -*-

{
    "name": "Rental Deposit",
    "summary": "A module to create an option to add deposit on a product when renting it.",
    "depends": ["sale_management", "website_sale_renting"],
    "data" : [
        'views/product_template_view.xml',
        'views/res_config_view_form.xml',
        'views/website_sale_renting_views.xml'
    ],
    'assets': {
        'web.assets_frontend': ['rental_deposit/static/src/js/website_sale_renting.js'],
    },
    "installable": True,
    "application": False,
    "license": "LGPL-3"
}
