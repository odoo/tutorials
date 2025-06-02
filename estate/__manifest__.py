{
    'name': 'estate',
    'depends': [
        'base',
    ],
    'data': [
        'models/estate_property_type.xml',
        'views/estate_property_type_views.xml',

        'models/estate_property.xml',
        'views/estate_property_views.xml',

        'views/estate_menus.xml',
        'security/ir.model.access.csv',

    ],

    'demo': [
        'demo/x_estate.property.type.csv',
        'demo/x_estate.property.xml',
    ],
    'license': 'LGPL-3',
}
