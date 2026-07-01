{
    'name': 'Real Estate',
    'author': 'Odoo S.A',
    'license': 'LGPL-3',
    'depends': ['base'],
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_propoerty_new_view.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tags_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_menus.xml',
    ],
    'demo': [
        'demo/estate_property_type_demo.xml',
        'demo/estate_property_tag_demo.xml',
        'demo/estate_property_demo.xml',
    ]
}
