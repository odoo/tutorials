{
    'name': "Real State",
    'version': '1.0',
    'depends': ['base'],
    'author': "kiro",
    'license': 'LGPL-3',
    'category': 'Real Estate/Brokerage',
    'description': """
    Description text
    """,
    'application': True,
    'installable': True,
    'auto_install': True,
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        
        'views/estate_property_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/res_users_views.xml',
        'views/estate_menus.xml',
    ],
    'demo': [
        'demo/estate.property.type.csv',
        'demo/estate.property.xml',
        'demo/estate.property.offer.xml'
    ]
}
