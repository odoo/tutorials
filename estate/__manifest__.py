{
    'name': 'Real Estate',
    'version': '1.0',
    'category': 'tutorials',
    'depends': ['base'],
    'summary': 'Chapter 2: Server Framework 101',
    'description': "",
    'installable': True,
    'application': True,
    'data': [
        'security/estate_security_access.xml',  
        'security/ir.model.access.csv',
        'views/estate_property_views.xml', 
        'views/estate_property_type_views.xml', 
        'views/estate_property_tag_views.xml', 
        'views/estate_menus.xml',
        'views/res_users_views.xml',
    ],
    'license':'LGPL-3'
}
