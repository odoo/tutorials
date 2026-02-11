{
    'name': "estate",
    'author': "pkhu",
    'license': "LGPL-3",
    'depends': ['base', 'mail'],
    'application': True,
    'category': 'Estate',
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_maintenance_view.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/res_users_views.xml',
        'views/estate_investor_views.xml',
        'views/estate_menus.xml',
        'data/mail_template.xml',
        'report/estate_property_report.xml',
        'report/estate_property_template.xml',
    ],
    'demo': [
        'data/property.xml'
    ],
}
