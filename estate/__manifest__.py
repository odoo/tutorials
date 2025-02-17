{
    'name': 'Estate',
    'category': 'Real Estate/Brokerage',
    'version': '1.0',
    'depends': ['base'],
    'license': 'LGPL-3',
    'application': True,
    'data':[
        'security/ir.model.access.csv',
        'report/estate_property_reports.xml',
        'report/estate_property_report_action.xml',
        'views/estate_property_inherit_res_user.xml',
        'views/estate_property_views.xml',
        'views/estate_property_offer.xml',
        'views/estate_property_type.xml',
        'views/estate_property_tag.xml',
        'views/estate_property_menus.xml'
    ],
    'demo':[
        'data/estate_property_demo.xml'
    ]
}
