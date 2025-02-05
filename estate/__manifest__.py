{
    'name' : 'estate',
    'depends' : ['base'],
    'application' : True,
    'installable' : True,
    'data' : [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml'
    ],
    'category' : 'Real Estate/Brokerage',
    'license': 'LGPL-3',
}
