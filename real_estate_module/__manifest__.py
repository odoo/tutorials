{
    'name': "Real Estate",
    'summary': "Manage real estate properties.",
    'description': "This is the real estate module used for buying and selling properties!",
    'version': '0.1',
    'application': True,
    'category': "Tutorials",
    'installable': True,
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'security/estate_property_rule_company.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        'views/res_user_views.xml',
        'data/estate_property_data.xml',
    ],
    'license': 'AGPL-3'
}
