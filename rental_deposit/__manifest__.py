{
    'name': 'Rental Deposit',
    'license': 'LGPL-3',
    'author': 'abpa',
    'summary': 'rental deposit for product',
    'depends': ['base', 'sale_renting', 'website_sale_renting'],
    'data': [
        'views/product_template_views.xml',
        'views/res_config_settings_views.xml',
        'views/templates.xml'
    ],
    'assets': {
        'web.assets_frontend': [
             'rental_deposit/static/src/website_sale.js'
        ]
    },
    'application': True,
    'installable': True,
}
