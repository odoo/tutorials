
{
    'name': 'Estate',
    'depends': [
        'base',
    ],
    'installable': True,
    'application': True,
    'data': [
        'views/estate_property_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_menus.xml',
        'security/ir.model.access.csv',

    ],
    'license': 'LGPL-3',
}
