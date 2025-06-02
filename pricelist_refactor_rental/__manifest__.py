{
    'name': 'Rental Pricelist Refactor',
    'version': '1.0',
    'category': 'Sales/Sales',
    'depends': ['sale_renting', 'sale', 'pricelist_refactor_base'],
    'description': """
        Refactors the pricelist functionality for Rental products, introducing discount and
        formula-based pricing rules.
    """,
    'data': [
        'views/product_pricelist_item_views.xml',
        'views/product_pricelist_views.xml',
        'views/product_template_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'installable': True,
    'license': 'OEEL-1',
}
