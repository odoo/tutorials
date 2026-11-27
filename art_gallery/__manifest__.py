{
    'name': 'Art Gallery',
    'version': '1.0',
    'summary': 'Manage the artworks of an art gallery',
    'application': True,
    'author': 'lobas',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/ir.access.csv',
        'views/art_gallery_artwork_views.xml',
        'views/art_gallery_menus.xml',
    ],
}
