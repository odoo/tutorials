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
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
         'views/res_users_views.xml',
        'views/estate_menus.xml',
        ],
    "license": "LGPL-3"
}
