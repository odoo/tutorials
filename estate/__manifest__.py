{
    'name': "Real estate",
    'version': "0.1",
    'depends': [
        'base'
        ],
    'descritpion': "A module for me to know how to develop modules at Odoo, also sell real estate",
    'author': "yagho",
    'application': True,
    'installable': True,
    'license': "LGPL-3",
    'data': [
        'security/ir.model.access.csv',
        'views/res_users_child_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_menu_views.xml',
    ]
}
