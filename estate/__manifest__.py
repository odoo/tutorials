{
    'name': 'Estate',
    "description": "This is a real estate listing module.",
    'version': '1.0',
    'depends': ['base'],
    'license': 'LGPL-3',
    'author' : 'Manthan Akbari',
     'data' : [
         'security/ir.model.access.csv',
         'views/estate_property_views.xml',
         'views/estate_menus.xml',
         ], 
     'application': True
}
