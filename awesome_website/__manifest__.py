{
    'name': "Awesome Website",

    'summary': """
        Companion addon for the Odoo JS Framework Training
    """,

    'description': """
        Companion addon for the Odoo JS Framework Training
    """,

    'author': "Odoo",
    'website': "https://www.odoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/19.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Tutorials',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['website'],
    'application': True,
    'installable': True,
    'data': [
        'data/images.xml',
        'views/snippets/snippets.xml',
        'views/snippets/s_image_comparison.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'awesome_website/static/src/interactions/**/*',
            'awesome_website/static/src/snippets/**/*.js',
        ],
    },
    'license': 'AGPL-3'
}
