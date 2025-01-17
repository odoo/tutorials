{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base', 'website'],
    'author': "Hitesh Prajapati",
    'category': 'Real Estate/Brokerage',
    'license': 'LGPL-3',
    'description': """
    Description text
    """,
    'application': True,
    'instalable': True,

    'data':[
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/res_users_views.xml',
        'wizard/estate_property_offer.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_details_template.xml',
        'views/estate_property_template.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menus.xml',
        'report/estate_property_templates.xml',
        'report/estate_property_reports.xml',
    ],
    'demo':[
        'data/estate.property.type.csv',
        'data/estate_property_data.xml',
        'data/estate_property_offer_data.xml',
    ]
    
}
