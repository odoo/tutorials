{
    "name": 'Catalog',
    "depends": ['stock'],
    "summary": "An app to create and manage product catalogs.",
    "data": [
        'security/ir.model.access.csv',
        'views/catalog_kanban_view.xml',
        'reports/catalog_report.xml',
        'views/catalog_views.xml',
        'views/catalog_menus.xml',
    ],
    'assets': {
    'web.assets_backend': [
        'catalog/static/src/views/**/*.xml',
        'catalog/static/src/views/**/*.js',
        ],
    },
    "installable": True,
    "application": True,
    "license": "LGPL-3"
}
