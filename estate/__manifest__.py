{
    'name':'estate',
    'category': 'Sales',
    'author' : 'shka',
    'summary': 'use to buy and sell properties ',
    'depends' : ['base'],
    'description': "buy and sell",
    'data':[
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_view.xml',
        'views/estate_menus.xml',
    ],
    'application' : True ,
    'installable' : True ,
    'auto_install' : True,
    'license': 'LGPL-3',
}
