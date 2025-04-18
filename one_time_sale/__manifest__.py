{
    'name': 'one_time_sale',
    'version': '1.0',
    'depends': ['sale_management', 'sale_subscription', 'website_sale'],
    'category': 'Sale',
    'summary': 'Sell products one time',
    'license': 'LGPL-3',
    'data': [
        'views/product_template_views.xml',
        'views/product_page_templates.xml',
    ],
    'installable': True,
    'auto_install': True,
    'application': True,
}
