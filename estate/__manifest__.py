{
    'name': 'Real Estate Advertisement',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Manage real estate listings and offers',
    'author': 'Anubhav Dubey',
    'depends': ['base'],  
    'data':[
        'security/ir.model.access.csv',
        'views/estate_menus.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
    ],
    'application': True,  
    'installable': True,  
    'license': 'LGPL-3', 
}


