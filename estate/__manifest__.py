{
    "name": "estate",
    "version": "1.0",
    "sequence": 1,
    "depends": ["base"],
    "description": "This module is used to manage real estate properties.",
    "installable": True,
    "application": True,
    'data' : [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        ],
    "license": "LGPL-3"
}
