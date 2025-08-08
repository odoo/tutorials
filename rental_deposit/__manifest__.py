{
    'name': "rental_deposit",
    'version': '18.0',
    'depends': ['sale_renting'],
    'author': "Smit",
    'category': 'Sales',
    'license' : 'LGPL-3',
    'description': """
        Deposit for rental products.
    """,
    'data': [
        'views/res_config_settings_views.xml',
        'views/product_template_views.xml',
        'views/templates.xml'
    ],
    'assets': {
        'web.assets_frontend': [
            'rental_deposit/static/src/js/rental_deposit_amount_qty.js',
        ],
    },
    'installable': True,
    'application': True,
}
