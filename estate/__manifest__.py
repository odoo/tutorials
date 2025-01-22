{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base'],

    'data' :[
        'security/ir.model.access.csv',

        # views
        'views/estate_property_views.xml',

        # menu
        'views/estate_menus.xml',

    ],
    'installable': True,
    'application': True,
}