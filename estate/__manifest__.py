{
    'name': 'Estate',
    'version': '1.0',
    'category': 'Estate',
    'summary': 'Estate application',
    'description': "",
    'website': 'https://www.odoo.com/page/estate',
    'depends': [
        'base',
    ],
    'data': [
        'views/res_users_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tags_views.xml',
        'views/estate_menus.xml',
        'security/ir.model.access.csv',
        ],
    'installable': True,
    'application': True,
}
