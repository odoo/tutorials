{
    "name" : "estate",
    "depends" : ['base','mail'],
    "category" : "Real Estate/Brokerage",
    'data' : [
        'views/res_users.xml',
        'data/estate_demo.xml',
        'demo/estate_demo_offer.xml',
        'views/estate_property_offer.xml',
        'views/estate_property_type.xml',
        'views/estate_property_tag.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': True,
}
