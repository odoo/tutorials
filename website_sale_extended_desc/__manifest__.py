# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Webshop Extended Description",
    'description': "Adds Extended Description field to view detailed information of product",
    'version': '1.0',
    'author': "nmak",
    'depends': ["website_sale"],
    'data': [
        'views/templates.xml',
        'views/product_views.xml'
    ],
    'installable': True,
    'license': "LGPL-3",
}
