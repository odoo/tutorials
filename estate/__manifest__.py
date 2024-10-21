{
    'name': "Estate",
    'version': '1.0',
    'depends': ['base', 'mail'],
    'author': "Odoo S.A.",
    'license': "LGPL-3",
    'category': 'Estate',
    'application': True,
    'auto_install': True,
    'description': """
    Tutorial app - Estate module
    """,
    # data files always loaded at installation
    'data': [
        'views/estate_property_view.xml',
        'views/estate_property_offer_view.xml',
        'views/estate_property_type_view.xml',
        'views/estate_property_tag_view.xml',
        'views/estate_menus.xml',
        'views/res_users_view.xml',
        'security/ir.model.access.csv',
        'data/estate_property_tag_data.xml',
        'data/estate_property_type_data.xml',
        'data/estate_property_data.xml',
        'data/estate_property_offer_data.xml',
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
        "demo/demo.xml",
    ],
}
