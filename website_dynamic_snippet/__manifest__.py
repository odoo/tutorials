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
            '/website_dynamic_snippet/static/src/js/layout_switcher.js',
        ],
        'website.assets_wysiwyg': [
            'website_dynamic_snippet/static/src/snippets/s_dynamic_sale_order_snippet/options.js',
        ]
    },
    'installable': True,
    'application': True,
}
