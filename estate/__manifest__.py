{
    "name": "Estate",
    "version": "1.0",
    "summary": "Estate Management",
    "author": "Arturo Yepez",
    "depends": ["base"],
    "application": True,
    "installable": True,
    "data": [
        'security/ir.model.access.csv',

        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ]
}