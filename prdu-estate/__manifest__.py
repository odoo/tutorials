{
    'name': "Estate module",
    'version': '0.1',
    'depends': ['base'],
    'author': "odoo.com",
    'category': 'Education',
    'description': """
    Lorem ipsum dolor sit amet
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menus.xml',
        'views/res_users_views.xml',
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
        'demo/demo_data.csv',
    ],
    'web.assets.common': [
        'web/static/css/*'
    ],
    'installable': True,
    'application': True,
    'license': "LGPL-3"
}
