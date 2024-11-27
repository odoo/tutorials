{
    'name': 'Estate',
    'version': '0.1',
    'depends': ['base'],
    'summary': 'Estate module',
    'category': 'Tutorials/Estate',
    'application': True,
    'license': 'AGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/res_users_views.xml',
        'data/master_data.xml',
    ],
    "demo": [
        "demo/demo_data.xml",
    ]
}
