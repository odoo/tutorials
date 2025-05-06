{
    'name': 'Better Ribbons',
    'version': '1.0',
    'description': 'Improved ribbons with badges and auto-assign',
    'author': 'Aryan Donga (ardo)',
    'license': 'LGPL-3',
    'depends': ['base', 'website_sale', 'website_sale_stock'],
    'installable': True,
    'auto_install': False,
    'data': [
        'views/product_ribbon_views.xml',
        'views/snippets.xml',
        'views/website_templates.xml',
    ],
    'assets': {
        'website.assets_wysiwyg': [
            'better_ribbons/static/src/js/website_sale_editor.js'
        ],
        'website.backend_assets_all_wysiwyg': [
            'better_ribbons/static/src/js/components/wysiwyg_adapter/wysiwyg_adapter.js'
        ],
    },
}
