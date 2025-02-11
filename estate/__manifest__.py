{
    "name" : "estate",
    "depends" : ['base'],
    "category" : "Real Estate/Brokerage",
    'data' : [
        'security/ir.model.access.csv',
        'security/security.xml',

        'views/res_users.xml',
        'views/estate_property_offer.xml',
        'views/estate_property_type.xml',
        'views/estate_property_tag.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml'
    ],
    'installable': True,
    'auto_install': True,
}
