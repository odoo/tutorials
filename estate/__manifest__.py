{
    'name': 'estate',
    'version': '1.0',
    'author' : "DhruvKumar Nagar",
    "description": "Real estate module for all your property needs!",
    'depends': [
        'base','sale'
    ],
    'installable': True,
    'application': True,
    'category': "Real Estate/Brokerage",
    'data': [
        'security/ir.model.access.csv',    
        'security/security.xml',
        'security/record_rules.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        'wizard/estate_property_offer_wizard_view.xml',
        'report/estate_property_offers_templates.xml',
        'report/estate_property_templates.xml',
        'report/estate_property_reports.xml',
        'report/res_users_templates.xml',
        'report/res_users_reports.xml',
    ],
    'demo':[
        'demo/estate_property_demo.xml'
    ]
}