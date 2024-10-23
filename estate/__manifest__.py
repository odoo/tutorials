{
    'name': "Real Estate",
    'description': "Create real estate properties and keep track of status",
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        'views/estate_property_types_views.xml',
    ],
    'license': "LGPL-3",
    # data files containing optionally loaded demonstration data
    'demo': [
        "demo/demo.xml",
    ],
}
