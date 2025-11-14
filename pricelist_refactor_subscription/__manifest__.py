{
    'name': 'Subscription Pricelist Refactor',
    'version': '1.0',
    'category': 'Sales/Subscriptions',
    'depends': ['product', 'sale_subscription', 'pricelist_refactor_base'],
    'description': """
        Refactors the pricelist functionality for subscription products, introducing discount and
        formula-based pricing rules.
    """,
    'data': [
        'views/product_pricelist_item_views.xml',
        'views/product_pricelist_views.xml',
        'views/product_template_views.xml',
    ],
    'pre_init_hook': '_pre_init_pricelist_refactor_sale_subscription',
    'installable': True,
    'license': 'OEEL-1',
}
