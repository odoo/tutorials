{
    'name' : 'estate',
    'version': '1.0',
    'summary':"It is a very useful app",
    'description' : "this is demo estate module",
    'category':'tools',
    'author': 'Abhishek patel',
    'license': 'LGPL-3',
    'depends': ['base'],
    'istallable': True,
    'application': True,

# this data fields loads the all required to run the module
    'data':[
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        ],


    
}