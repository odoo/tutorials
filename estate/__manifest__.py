{
    'name':'estate',
    'version': '1.0',
    'category':'Real Estate/Brokerage',
    'author': "assh-odoo",
    'depends':['base', 'mail'],
    'data':[
        'security/security.xml',
        'security/ir.model.access.csv',
        'security/estate_property_security.xml',
        'data/estate.property.types.csv',
        'report/estate_property_template.xml',
        'report/estate_property_reports.xml',
        'report/res_users_template.xml',
        'report/res_users_reports.xml',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_types_views.xml',
        'views/estate_property_tags_views.xml',
        'views/estate_users_views.xml',
        'views/estate_property_offer_wizard_view.xml',
        'views/estate_property_template.xml',
        'views/estate_menus.xml',
    ],
    'demo':[
        'demo/estate.property.xml',
        'demo/estate.property.offer.xml'
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3'
}
