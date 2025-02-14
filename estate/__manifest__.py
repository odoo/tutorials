{
    'name': 'Real estate',
    'version': '1.0',
    'author' : "sujal asodariya",
    "description": "Real estate module for managing property listings and transactions!",
    'category': 'Real Estate/Brokerage',
    'depends': [
        'base',
        'mail'
    ],
    "demo": ["demo/estate_demo_data.xml"],
    'data':[
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/estate_property_type.xml',
        'report/estate_property_reports.xml',
        'report/estate_property_templates.xml',
        'report/estate_property_subtemplate.xml',
        'report/estate_property_user_template.xml',
        'views/res_users_views.xml',
        'views/estate_property_offer.xml',
        'views/estate_property_type_view.xml',
        'views/estate_property_tags.xml',
        'views/estate_property_views.xml',  
        'views/estate_menus.xml',
        'views/estate_property_report_inherit.xml'
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}