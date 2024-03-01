{
    'name': 'Estate',
    'version': '1.0',
    'category': 'Real Estate/Brokerage',
    'summary': 'Estate application',
    'description': "",
    'website': 'https://www.odoo.com/page/estate',
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/res_users_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tags_views.xml',
        'views/estate_menus.xml',
        ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
