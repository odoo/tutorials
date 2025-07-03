{
    'name': 'Case Study: Javascript',
    'depends': [
        'point_of_sale',
    ],
    'application': True,
    'installable': True,
    'data': [
        'views/pos_config_views.xml'
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'case_javascript/static/src/**/*',
        ]
    },
    'license': 'AGPL-3',
}
