{
    "name" : "estate",
    "depends" : ['base'],
    'data' : [
        'security/ir.model.access.csv',

        'views/estate_property_offer.xml',
        'views/estate_property_type.xml',
        'views/estate_property_tag.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml'
    ],
    'installable': True,
    'auto_install': True,
}
