{
    'name': 'Real Estate',
    'depends': ['base'],
    'category': 'Tutorials',
    'application': True,
    'data': ['data/ir.model.access.csv',
             'views/res_users.xml',
             'views/estate_property_offer_views.xml',
             'views/estate_property_views.xml',
             'views/estate_property_type_views.xml',
             'views/estate_property_tag_views.xml',
             'views/estate_menus.xml',
             ],
    'demo': [
        "demo/demo.xml",
    ],
    'license': 'AGPL-3'
}
