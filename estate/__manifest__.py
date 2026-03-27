{
    'name': 'Estate',
    'version': '1.0',
    'author': 'Odoo S.A.',
    'license': 'AGPL-3',
    'installable': True,

    'depends': ['base'],

    'category': 'Real Estate/Brokerage',

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/estate_property_offers_views.xml',
        'views/estate_property_types_views.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        'views/res_users_views.xml',
        'data/estate_property_type_data.xml',
    ],

    'demo': [
        'demo/estate_property_partners_demo_data.xml',
        'demo/estate_property_demo_data.xml',
        'demo/estate_property_offer_demo_data.xml',
    ],
}
