{
    'name': 'Estate',
    'version': '1.0',
    'depends': ['base', 'mail'],
    'application': True,
    'installable': True,
    'author': "vivah",
    'category': 'Tutorials',
    'license': 'AGPL-3',
    'data': [
        'data/email_template_visit_reminder.xml',
        'data/visit_reminder_cron.xml',
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_visit_views.xml',
        'views/estate_menus.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_tag_views.xml',
        'views/res_users_view.xml',
    ]
}
