{
    'name': 'one_time_sale',
    'version': '1.0',
    'depends': ['website', 'sale_management', 'sale_subscription', 'website_sale'],
    'category': 'Sale',
    'summary': 'Sell products one time',
    'license': 'LGPL-3',
    'data': [
        'views/product_template_views.xml',
        'views/product_page_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'one_time_sale/static/src/js/product_subscription.js',
        ],
    },
    'installable': True,
    'auto_install': True,
    'application': True,
}
