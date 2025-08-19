{
    'name': 'Custom Catalog View',
    'version': '1.0',
    'summary': 'Redesigned mobile catalog view with large images and popup zoom',
    'author': 'Dijo',
    'license': 'LGPL-3',
    'depends': ['sale_management', 'product'],
    'data': [
        'views/catalog_product_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'redesing_catalog/static/src/js/image_popup.js',
            'redesing_catalog/static/src/js/image_template.xml',
            'redesing_catalog/static/src/css/product_kanban.scss',
        ],
    },
}
