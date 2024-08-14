{
    'name': 'ESTATE',
    'version': '1.2',
    'description': "",
    'depends': [
        'base_setup',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_menu.xml',
        'views/estate_property_offer_view.xml',
        'views/estate_property_type_view.xml',
        'views/estate_property_type_menu.xml',
        'views/estate_property_tag_view.xml',
        'views/estate_property_tag_menu.xml',
        'views/res_users_view.xml'
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3'
}
