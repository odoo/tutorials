{

    "name" : "rental_deposit",
    "version": "1.0",
    'depends': ["sale_management", "website_sale_renting"],
    "installable" : True,
    "application" : False,
    'license' : "LGPL-3",
    'data' : [
        "views/product_template_views.xml",
        "views/website_sale_template_views.xml",
        "views/res_config_settings_views.xml",
    ]
} 
