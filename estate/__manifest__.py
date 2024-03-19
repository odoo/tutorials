# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "Clément Cardot (cacl)",
    'license': "LGPL-3",
    'description': """
        A new app to learn the Odoo framework
    """,

    'data': [
        'security/ir.model.access.csv',

        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ],

    'application': True,
}
