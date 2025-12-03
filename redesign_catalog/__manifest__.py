{
    'name': 'Redesign Catalog View',
    'version': '1.0',
    'summary': 'Redesign Catalog View',
    'author': 'Raghav Agiwal',
    'depends': ['sale_management', 'stock'],
    'data': [
        'views/product_template_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'redesign_catalog/static/src/scss/image_style.scss',
            'redesign_catalog/static/src/component/product_image_popup.js',
        ],
    },
    'installable': True,
    'auto_install': True,
    'license': 'LGPL-3'
}
