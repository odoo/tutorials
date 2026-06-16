{
    'author': 'Aditi (adpaw)',
    'name': 'Deposit Rental App',
    'license': 'LGPL-3',
    'depends': ['sale_renting', 'website_sale'],
    'data': [
        'views/res_config_settings_view.xml',
        'views/product_template_view.xml',
        'views/template_view.xml'
    ],
    'assets': {
        'web.assets_frontend': [
            'rental_deposit/static/src/deposit_amount.js',
        ],
    },
    'installable': True,
    'auto_install': True,
}
