{
    'name': "estate",
    'depends': ['base_setup'],
    'description': "Technical practice",
    'installable': True,
    'application': True,

     'data': [
         'security/ir.model.access.csv',
         'views/estate_property_views.xml',
         'views/estate_menus.xml'
             ],
}
