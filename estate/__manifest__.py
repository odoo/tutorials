{
    'name': "Real Estate",
    'version': '1.0',
    'summary'  "Manage properties and buyers."
    'depends': [
        'base'
    ],
    'author': "wimar-odoo",
    'description': """
    Manage efficiently real estate properties for sale and match them with potential buyers.",
    """,
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ],
}
