{
    'name': 'estate',
    'version': '1.0',
    'author' : "DhruvKumar Nagar",
    "description": "Real estate module for all your property needs!",
    'depends': [
        'base',
    ],
    'installable': True,
    'application': True,
    'data': [
        'security/ir.model.access.csv',    
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ],
    'demo':[
        'demo/estate_property_demo.xml'
    ]
}