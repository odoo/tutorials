{
    'name': 'estate',
    'category': 'real estate',
    'summary': 'create a estate property',
    'website': 'https://www.odoo.com',
    'depends': ['base'],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'data': [
    'security/ir.model.access.csv',
    'views/estate_property_views.xml',
    'views/estate_property_offer_views.xml',
    'views/estate_property_type_views.xml',
    'views/estate_property_tags_views.xml',
    'views/estate_property_resusers_views.xml',
    'views/estate_menus.xml',
    'data/estate_property_type_data.xml',
    'report/ estate_property_reports.xml',
    'report/ estate_property_templates.xml'
    ],
    'demo':[
        'demo/estate_demo_data.xml',
        'demo/estate_offer_demo_data.xml',
    ],
}