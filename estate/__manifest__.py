{
    'name':'estate',
    'author':'dijo',
    'version':'1.2',
    'summary':'This is real-estate module developed by deep i. joshi',
    'application': True,
    'depends': ['base','mail','whatsapp','website'],
    'category':'Real Estate/Brokerage',
    'license': 'LGPL-3',
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv', 
        'data/property_type_data.xml',
        'data/email_template.xml',
        'data/whatsapp_template.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/res_user_view.xml',
        'views/controller_view.xml',
        'views/controller_property_page.xml',
        'wizard/estate_property_wizard.xml',
        'views/estate_property_views.xml',
        'report/estate_property_templates.xml',
        'report/estate_property_reports.xml',
        'views/estate_property_menu.xml',
    ],
    'demo': [
        'demo/property_demo_date.xml'
    ]
}
