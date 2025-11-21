{
    'name': "Deposit Rental Products",
    'depends': ['sale_renting', 'website_sale'],
    'application': False,
    'installable': True,
    'license': 'LGPL-3',
    'data': [
        'views/product_template_views.xml',
        'views/res_config_settings_views.xml',
        'views/templates.xml',
        'views/sale_order_view.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'deposit_renting/static/src/js/product_deposit.js',
        ],
    }
}
