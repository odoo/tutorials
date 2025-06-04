{
    'name': 'ESTATE',
    'description': "aras estate tutorial module",
    'website': 'https://www.odoo.com/page/estate',
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_menus.xml',
        'views/res_users_views.xml',
    ],
    'demo': [
        'demo/estate.property.type.csv'
    ],
    'installable': True,
    'application': True,
}
