{
    'name': 'Real Estate',
    'version': '1.0',
    'summary': 'Manage real estate properties',
    'description': 'Module to manage real estate properties',
    'author': 'Akya',
    'category': 'Real Estate/Brokerage',
    'sequence': '15',
    'depends': ['base', 'mail','website'],
    'data': [
        'security/estate_security.xml',
        'security/ir.model.access.csv',
        'data/estate.property.type.csv',
        'wizard/estate_property_offer_wizard.xml',        
        'wizard/estate_property_event_view.xml',
        'views/estate_property_views.xml',
        'views/estate_property_controller_template.xml',
        'views/estate_property_offer_view.xml',
        'views/estate_property_tag_view.xml',
        'views/estate_property_type_view.xml',
        'views/res_users_view.xml',
        'views/estate_menus.xml',
        'report/estate_property_reports.xml',
        'report/estate_property_templates.xml',
    ],
    'demo':[
        'demo/estate_property_demo.xml'
    ],
    'installable': True,
    'application': True,
    'license': 'AGPL-3'
}
