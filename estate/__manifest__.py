{
    'name': 'Real estate',
    'version': '1.0',
    'author' : "sujal asodariya",
    "description": "Real estate module for managing property listings and transactions!",
    'category': 'Real Estate/Brokerage',
    'depends': [
        'base',
        'mail'
    ],
    'data':[
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/estate_property_type.xml',
        'views/res_users_views.xml',
        'views/estate_property_offer.xml',
        'views/estate_property_type_view.xml',
        'views/estate_property_tags.xml',
        'views/estate_property_views.xml',  
        'views/estate_menus.xml',
    ],
    "demo": ["demo/estate_demo_data.xml"],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}