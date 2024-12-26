{
    'name': 'estate',
    'version': '1.0',
    'author' : 'Dhruv Chauhan',
    'description': 'Real estate module for managing property listings and transactions!',
    'depends': [
        'base'
    ],
    'data':[
        'security/security.xml',
        'data/estate_property_type_demo.xml',
        'data/estate_property_demo.xml', 
        'data/estate_property_offer_demo.xml',  
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menus.xml',
        'views/res_users_views.xml'
    ],
    'installable': True,
    'application': True,
    'category': 'Real Estate/Brokerage',
    'license': 'LGPL-3', 
}
