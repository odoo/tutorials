{
    'name': 'Estate',
    'depends': [
        'base_setup'],
    'application': True,
    'data': [
        'security/ir.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_tags_views.xml',
        'views/estate_property_types_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_menus.xml'
    ],
    'author': 'frpmneto',
    'license': 'LGPL-3'
}
