{
    'name': 'Real Estate',
    'version': '1.0',
    'category': 'Real Estate',
    'summary': 'Manage real estate advertisements and offers',
    'author': 'Khushi',
    'depends': ['base','web'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'estate/static/description/icon.png',
        ],
    },
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
