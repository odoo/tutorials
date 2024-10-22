{
    'name': "Real State",
    # 'version': '1.0',
    'depends': ['base'],
    'author': "Sahil Mangukiya",
    # 'category': 'Category',
    'description': "This is my First tutorial module.",
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        
        'views/res_users_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_views.xml',
        'views/estate_menu.xml'
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}