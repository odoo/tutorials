{
    "name": "Estate",
    "version": "1.0",
    "summary": "Estate Management",
    "depends": ["base"],
    "application": True,
    "installable": True,
    "data": [
        'security/ir.model.access.csv',

        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_menus.xml',
    ],
    "author": "Arturo Yepez",
    "license": 'LGPL-3',
}
