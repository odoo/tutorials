{
    'name': "Real Estate",
    'version': '1.0',
    'author': "Odoo S.A.",
    'summary': "Estate management",
    'description': """Estate Property Module""",
    'depends': ['base'],
    'category': 'Real Estate/Brokerage',
    'data': [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_menus.xml",
    ],
    'license': 'LGPL-3',
    'application': True,
    'installable': True
}
