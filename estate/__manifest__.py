{
    'name': 'estate',

    'category': 'real estate',

    'summary': 'create a estate property',

    'website': 'https://www.odoo.com',

    'depends': ['base'],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',

    'data': [
    'security/ir.model.access.csv',
    'views/estate_property_views.xml',
    'views/estate_property_type_views.xml',
    'views/estate_property_tags_views.xml',
    #'views/estate_property_offer_views.xml',
    'views/estate_menu_type_xml',
    'views/estate_best_views.xml',
    'views/estate_menus.xml'
    ],

}