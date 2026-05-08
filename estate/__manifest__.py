{
    'name': 'Real Estate',
    'summary': 'Manage real estate properties and offers',
    'description': "This module allows managing property advertisements,including property details, offers, and related data.",
    'author': 'Sudarshan Maity (sumai)',
    'website': '',
    'category': 'Real Estate',
    'version': '1.0',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mail',
        'crm',
        ],

    'data': [
        'security/ir.model.access.csv',
        'data/mail_template.xml',
        'data/offer_cron.xml',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_visit_views.xml',
        'views/estate_property_issue_views.xml',
        'views/res_users_views.xml',
        'views/estate_menus.xml',
    ],

    'installable': True,
    'application': True,
}
