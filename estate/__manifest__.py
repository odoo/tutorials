{
    "name": "Real Estate",
    "description": "",
    "depends": ['base'],
    "sequence": 1,
    "license": "LGPL-3",
    "application": True,
    "installable": True,
    "data" : [
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        'security/ir.model.access.csv',
    ]
}