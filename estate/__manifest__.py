{
    'name': 'Estate',
    'description': 'A module to manage real estate advertisments',
    'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menus.xml',
        'views/estate_property_offer_view.xml'
    ],

    'installable': True,
    'application': True,
    'license': 'AGPL-3',
}
