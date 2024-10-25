{
    'name': "Real State",
    'depends': ['base'],
    'author': "Sahil Mangukiya",
    'category': 'Real Estate/Brokerage',
    'description': "This is my First tutorial module.",
    'data': [
        'security/estate_security.xml',
        'security/ir.model.access.csv',
        'data/estate.property.type.csv',
        'views/res_users_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_views.xml',
        'views/estate_menu.xml'
    ],
    'demo': [
        'demo/estate_property_demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}
