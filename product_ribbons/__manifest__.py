{
    'name': 'Product Ribbon Manager',
    'version': '1.0',
    'summary': 'Dynamic Ribbon (Badge) for Products like Out of Stock, Sale, New, Custom',
    'author': 'Mandani Tushar',
    'category': 'Website',
    'depends': ['website_sale'],
    'assets': {
        'website.assets_wysiwyg': [
            'product_ribbons/static/src/js/website_sale_editor_extend.js',
        ],
        'website.backend_assets_all_wysiwyg': [
            'product_ribbons/static/src/js/adapter.js']
    },
    'data': [
        'views/product_ribbons.xml',
        'views/product_ribbon_web_editor.xml'
    ],
    'license': 'LGPL-3',
}
