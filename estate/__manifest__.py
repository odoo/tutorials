{
    'name': 'estate',
    'license': 'LGPL-3',
    'depends': [
        'base',
    ],
    'data': [
        'models/model_real_estate_property_type.xml',
        'models/model_real_estate_property_tag.xml',
        'models/model_real_estate_property_offer.xml',
        'models/model_real_estate_property.xml',
        'security/ir.model.access.csv',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ],
    "installable": True,
    "application": True,
}
