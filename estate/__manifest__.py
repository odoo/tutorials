{
    'name': 'Real Estate',
    'author': 'Aditi (adpaw)',
    'license': 'LGPL-3',
    'depends': [
        'base', 'calendar', 'mail', 'event'
    ],
    'data': [
        'security/estate_security.xml',
        'security/ir.model.access.csv',
        'data/mail_template.xml',
        'views/estate_property_visit_views.xml',
        'views/estate_property_tags_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_types_views.xml',
        'views/estate_property_issues_views.xml',
        'views/res_user.xml',
        'views/estate_property_views.xml',
        'views/estate_property_menus.xml',
    ],
    'installable': True,
    'application': True,
}
