# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Real Estate",
    'version': "0.1",
    'depends': ['base'],
    'author': "Odoo",
    'category': "Real Estate/Brokerage",
    'description': """
        A Real Estate management app
    """,
    'application': True,
    'installable': True,
    'license': "AGPL-3",
    'data': [
        "security/ir.model.access.csv",
        "security/security.xml",
        "views/estate_property_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/res_users_views.xml",
        "views/estate_menus.xml",
    ],
}
