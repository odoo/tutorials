{
    'name': 'estate',
    'depends': [
        'base',
    ],
    'data': [
        'models/estate_models.xml',

        'models/fields/estate_property_type.xml',
        'views/estate_property_type_views.xml',

        'models/fields/estate_property_tag.xml',
        'views/estate_property_tag_views.xml',

        'models/fields/estate_property_offer.xml',
        'views/estate_property_offer_views.xml',

        'models/fields/estate_property.xml',
        'views/estate_property_views.xml',

        'views/estate_menus.xml',
        'security/ir.model.access.csv',

    ],

    'demo': [
        'demo/x_estate.property.type.csv',
        'demo/x_estate.property.tag.csv',
        'demo/x_estate.property.xml',
    ],
    'license': 'LGPL-3',
}
