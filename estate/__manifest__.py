{
    'name': 'Real Estate',
    'description': 'Buy and sell Real Estate properties',
    'license':'GPL-3',
    'depends': [
        'base'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_types_view.xml',
        'views/estate_property_tag_view.xml',
        'views/estate_property_offers_view.xml',
        'views/estate_menus.xml',
    ],
    'installable': True,
    'application': True
}
