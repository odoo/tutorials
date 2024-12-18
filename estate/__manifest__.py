{
    'name': 'estate',
    'version': '1.0',
    'author' : "Dhruv Chauhan",
    "description": "Real estate module for managing property listings and transactions!",
    'depends': [
        'base'
    ],
    'installable': True,
    'application': True,
    'category': "Real Estate/Brokerage",
    'license': "LGPL-3",
    'data':[
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_menus.xml'       
    ],
}
