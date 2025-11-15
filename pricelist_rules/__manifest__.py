# Part of Odoo. See LICENSE file for full copyright and licensing details.  

{
    'name': "Pricelist Rules",
    'category': 'Sales/Sales',
    'description': """
This module extends the Pricelist functionality for Sale, Rental, and Subscription. 
""",
    'version': "1.0",
    'author': "praj-odoo",
    'depends': ['product','sale_renting', 'sale_subscription'],
    'data': [
        'views/product_template_views.xml',
        'views/product_pricelist_views.xml',
        'views/sale_subscription_product_pricelist_item_view.xml',
        'views/sale_renting_product_pricelist_views.xml',
        'views/sale_renting_product_template_views.xml',
        'views/sale_subscription_product_template_views.xml'         
    ],
    'installable': True,
    'license': "OEEL-1"
}
