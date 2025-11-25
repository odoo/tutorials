{
    'name': "Real Estate",

    'summary': "Cool Real Estate App",
    'description': """
Cool Real Estate App
Wow This is a description omgg
    """,
    'author': "kmhma",
    'website': "https://www.odoo.com/",
    'category': 'Tutorials',
    'version': '0.1',
    'application': True,
    'installable': True,
    'depends': ['base'],

    'data': [
        "security/ir.model.access.csv",
        "views/property_type_views.xml",
        "views/property_tag_views.xml",
        "views/property_offer_views.xml",
        "views/estate_property_views.xml",
        "views/res_users_views.xml",
        "views/estate_menus_views.xml",
    ],
    'license': 'LGPL-3',
}
