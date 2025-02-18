{
    'name': 'Real Estate',
    'version': '1.0',
    'category': 'Real Estate/Brokerage',   
    'depends': ['base','mail'],
    'data': [
        'report/estate_property_template.xml',
        'report/estate_property_report.xml' ,
        'security/security.xml', 
        'security/ir.model.access.csv',
        'views/estate_property_offer_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_views.xml',
        'views/res_users_inherited_views.xml',
        'views/estate_menus.xml',
        'data/estate.property.type.csv',
        'demo/estate_property_demo.xml'
    ],
    'installable': True,
    'application': True
}

