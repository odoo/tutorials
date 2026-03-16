{
    'name': "Real Estate",
    'version': "1.0",
    'category': "Real Estate",
    'summary': "Manage real estate properties",
    'description': "This module allows managing properties",
    'depends': ['base', 'mail', 'website'],
    'author': "jakan",
    'license': "LGPL-3",
    'application': True,
    'installable': True,
    'data': [
        "security/ir.model.access.csv",
        "views/templates.xml",
        "views/estate_property_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_maintenance_views.xml",
        "views/estate_property_investor_views.xml",
        'views/res_users_views.xml',
        "views/estate_menus.xml",
        "views/snippets/s_real_estate_snippets.xml",
        "views/snippets/snippets.xml",
    ],
    'assets': {
        'web.assets_frontend': [
            'estate/static/src/scss/s_real_estate.scss',
            'estate/static/src/builder/estate_snippet_option_plugin.js',
        ],
        'website.assets_editor': [
            'estate/static/src/builder/estate_snippet_option.xml',
        ],
    },
    'demo': [
        "data/estate_property_default.xml",
    ],
}
