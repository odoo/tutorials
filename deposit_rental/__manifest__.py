{
    'name': 'Rental Product Deposit',
    'version': '1.0',
    'category': 'Sales/Rental',
    'summary': 'Adds mandatory deposit option for rental products',
    'description': """
        This module introduces a mandatory deposit feature for rental products,
        allowing the configuration of a deposit amount per product and
        handling it in both backend and frontend rental flows.
    """,
    'author': 'Your Name',
    'depends': ['base', 'sale_renting', 'website_sale_renting'],
    'data': [
        'views/res_config_settings_views.xml',
        'views/product_template_views.xml',
        'views/website_sale_renting_template.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
