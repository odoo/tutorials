{
    'name': 'estate',
    'version': '1.0',
    'author' : 'Dhruv Chauhan',
    'description': 'Real estate module for managing property listings and transactions!',
    'depends': [
        'base',
        'mail'
    ],
    'data':[
        'security/security.xml',
        'security/ir.model.access.csv',

        'data/mail_template_data.xml',

        'wizard/estate_multiple_offer_views.xml',

        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menus.xml',
        'views/res_users_views.xml',

        'report/estate_property_sub_templates.xml',
        'report/estate_property_offers_template.xml',
        'report/estate_property_reports.xml',
        'report/estate_user_property_template.xml',
        'report/estate_property_user_reports.xml',
    ],
    'demo': [
        'data/estate_property_type_demo.xml',
        'data/estate_property_demo.xml', 
        'data/estate_property_offer_demo.xml',  
    ],
    'installable': True,
    'application': True,
    'category': 'Real Estate/Brokerage',
    'license': 'LGPL-3', 
}
