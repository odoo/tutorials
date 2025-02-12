{
    "name" : "estate",
    "depends" : ['base'],
    "category" : "Real Estate/Brokerage",
    'data' : [
        'views/res_users.xml',
        'views/estate_property_offer.xml',
        'views/estate_property_type.xml',
        'views/estate_property_tag.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
    ],
    'demo':[
        'data/estate_demo.xml',
    ],
    'installable': True,
    'auto_install': True,
}
