{
    'name': 'Website Dynamic Snippet',
    'version': '18.4.1.0.0',
    'category': 'Website',
    'depends': ['website_sale'],
    'data': [
        'views/snippets/snippets.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'website_dynamic_snippet/static/src/snippets/s_dynamic_sale_order_snippet/000.xml',
            'website_dynamic_snippet/static/src/snippets/s_dynamic_sale_order_snippet/000.js',
        ],
        'website.assets_wysiwyg': [
            'website_dynamic_snippet/static/src/snippets/s_dynamic_sale_order_snippet/options.js',
        ],
        'web.assets_tests': [
            'website_dynamic_snippet/static/tests/tours/dynamic_snippet_tour.js',
        ],
    },
    'installable': True,
    'application': True,
}
