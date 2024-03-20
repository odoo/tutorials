{
    'name': 'Real Estate',
    'depends': [
        'base',
    ],
    'application': True,
    'description': '',
    'data': ['security/ir.model.access.csv',
             'views/estate_property_offer_views.xml',
             'views/estate_property_views.xml',
             'views/estate_property_type_views.xml',
             'views/estate_property_tag_views.xml',
             'views/estate_menus.xml'],
    'license': 'LGPL-3'
}
