{
    'name' : "estate",
    'version' : '1.0',
    'depends' : ['base', 'mail'],
    'category' : 'Real Estate',
    'description' : 'A module for managing real estate properties!',
    'installable' : True,
    'application' : True,
    'data': [
       'security/estate_security.xml',
       'security/ir.model.access.csv',
       'security/ir_rule.xml',
       'views/estate_property_offer_views.xml',
       'views/estate_property_views.xml',
       'views/estate_property_type_views.xml',
       'views/estate_property_tag_views.xml',
       'views/res_users_views.xml',
       'views/estate_menu.xml',
       'report/estate_property_offer_report.xml',
       'report/estate_property_offer_templates.xml',
    ],
    'demo' : [
        'data/estate_demo.xml',
    ],
    'license': 'AGPL-3'
}
