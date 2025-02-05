{
    'name': 'Real Estate Advertisement',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Manage real estate listings and offers',
    'author': 'Anubhav Dubey',
    'website': 'http://localhost:8069',
    'depends': ['base'],  
    'data':[
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        #'views/estate_property_views_list.xml',
        'views/estate_menus.xml',
        
    ],
    'application': True,  
    'installable': True,  
}

