{
    'name': 'Website Dynamic Snippet',
    'version': '18.0.1.0.0',
    'category': 'Website',
    'depends': ['website_sale'],
    'data': [
        'views/snippets/snippet_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            '/website_dynamic_snippet/static/src/xml/sale_order_snippets.xml',
            '/website_dynamic_snippet/static/src/js/dynamic_snippet_sale_orders.js',
        ],
    },
    'installable': True,
    'application': True,
}
