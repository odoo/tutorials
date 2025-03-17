{
    'name': 'Pricelist Refactor',
    'version': '1.0',
    'category': 'sale_management',
    'depends': ['sale_subscription', 'sale_renting'],
    'description': """
        Refactors the pricelist functionality for rental and subscription products, introducing discount and 
        formula-based pricing rules.
    """,
    'data': [
        'views/product_pricelist_views.xml',
        'views/product_pricelist_item_views.xml',
        'views/product_template_views.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}
