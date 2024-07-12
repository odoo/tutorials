{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "Ashutosh Yadav",
    'category': 'Real Estate',
    'description': """
    Description text
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'views/res_users.xml',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menus.xml'
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
    ],
    'installable': True,
    'application': True,
    'license': 'AGPL-3'
}
