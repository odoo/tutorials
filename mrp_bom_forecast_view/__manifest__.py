
{
    'name': 'BoM Clean Forecast Overview',
    'version': '1.0',
    'depends': [
        'base',
        'mrp'
    ],
    'author': 'Sanket Tank',
    'category': 'Manufacturing/Manufacturing',
    'description': '''
    This module will modify current BoM Overview and make it clean and optimist.
    ''',
    'assets': {
        'web.assets_backend': [
            'mrp_bom_forecast_view/static/src/**/*',
        ],
    },
    'license': 'LGPL-3',
    'installable': True,
    'application': True
}
