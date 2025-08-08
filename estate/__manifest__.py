{
    'name': "Real Estate",
    'summary': """
        Real Estate Tutorial Project
    """,
    'description': """
        Real Estate Tutorial Project
    """,
    'author': "Odoo",
    'website': "https://www.odoo.com/",
    'category': 'Tutorials/Real Estate',
    'version': '1.0',
    'application': True,
    'installable': True,
    'depends': ['base'],
    'data': [
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/res_users_views.xml",
        "views/estate_menus.xml",
    ],
    'license': "LGPL-3",
}
