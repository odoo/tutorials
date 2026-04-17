{
    'name': 'Estate',
    'summary': 'Manage properties listing and offers',
    'description': "A simple module to manage real estate properties and track offers made by buyers.",
    'author': 'Mohit Ahir (moahi)',
    'website': '',
    'category': 'Estate',
    'version': '1.0',
    'license': 'LGPL-3',
    'depends': ['base', 'calendar'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_offer_views.xml',
        'views/esate_property_issue_views.xml',
        'views/estate_property_visit_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_tags_views.xml',
        'views/estate_menus.xml',
        'views/res_users_views.xml'
    ],
    'installable': True,
    'application': True,
}
