{
    'name': 'estate',
    'version': '0.1',
    'license': 'LGPL-3',
    'depends': ['base_setup', 'mail'],
    'description': "Technical Training",
    'installable': True,
    'application': True,

    'data': [
        'security/ir.model.access.csv',
        'view/res_user_views.xml',
        'view/estate_property_views.xml',
        'view/estate_property_offer_views.xml',
        'view/estate_property_type_views.xml',
        'view/estate_property_tag_views.xml',
        'view/estate_menus.xml',
        ],
}
