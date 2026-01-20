# -*- coding: utf-8 -*-
{
    'name': 'Redesign Catalog View',
    'version': '1.0',
    'depends': ['product'],
    'data': [
        'views/product_kanban_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'redesign_catalog_view/static/src/scss/product_kanban.scss',
            'redesign_catalog_view/static/src/js/image_preview_widget.js',
            'redesign_catalog_view/static/src/js/image_preview_widget.xml',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
