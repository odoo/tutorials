{
    'name': 'Ribbon',
    'version': '1.0',
    'summary': '',
    'author': 'PBCH',
    'category': 'Website',
    'depends': ['website_sale', 'stock'],
    'data': [
        'views/product_ribbon_view.xml',
        'views/snippet.xml',
    ],
    'assets': {
        'website.assets_wysiwyg': [
            'dynamic_ribbons/static/src/js/website_sale_editor.js',
        ],
        'website.backend_assets_all_wysiwyg': [
            'dynamic_ribbons/static/src/js/adapter.js',
        ],
    },
    'license': 'LGPL-3',
}
