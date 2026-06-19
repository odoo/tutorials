{
    'name': 'Library',
    'version': '1.0',
    'category': 'Tutorials',
    'author': 'times',
    'description': 'Library Management',
    'summary': 'Library Management',
    'depends': ['base', 'account'],
    'license': 'LGPL-3',
    'application': True,
    'installable': True,
    'data': [
        'security/ir.model.access.csv',
        'views/library_book_views.xml',
        'views/library_borrow_views.xml',
        'views/library_member_views.xml',
        'views/library_waive_wizard_views.xml',
        'views/library_menus.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'library/static/src/js/library_return_notif.js',
            'library/static/src/components/**/*',
            'library/static/src/components/counter_widget.js',
            'library/static/src/components/counter_widget.xml',
        ]
    }
}
