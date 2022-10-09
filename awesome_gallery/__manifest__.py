# -*- coding: utf-8 -*-
{
    'name': "Gallery View",
    'summary': "Defines the 'gallery' view",
    'description': """
        Defines a new type of view ('awesome_gallery') which allows to visualize images.
    """,

    'version': '0.1',
    'depends': ['web'],
    'data': [],
    'assets': {
        'web.assets_backend': [
            'awesome_gallery/static/src/**/*',
        ],
    },
    'license': 'AGPL-3'
}
