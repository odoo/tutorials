{
    'name':'estate',
    'version': '1.0',
    'category':'Real Estate/Brokerage',
    'author': "assh-odoo",
    'depends':[
        'base'
    ],
    'data':[
        'security/security.xml',
        'security/ir.model.access.csv',
        'security/estate_property_security.xml',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_types_views.xml',
        'views/estate_property_tags_views.xml',
        'views/estate_users_views.xml',
        'views/estate_menus.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3'
}
