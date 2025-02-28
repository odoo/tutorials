# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Deposit for rental products",
    'description': "Adds deposit management to rental products",
    'version': '1.0',
    'author': "nmak",
    'depends': ["sale_renting", "website_sale"],
    'data': [
        'views/product_template_views.xml',
        'views/website_sale_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'installable': True,
    'license': "LGPL-3",
}
