{
    'name': 'Awesome Estate',
    'version': '0.1',
    'category': 'Tutorials',
    'summary': 'Real Estate Advertisement tutorial module',
    'description': """
Real Estate Advertisement Management Module

Manage property listings, offers, property types, and tags.
Supports the full property lifecycle: new, offer received, offer accepted, sold, and canceled.
    """,
    'author': 'Patja',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/awesome_estate_security.xml',
        'security/ir.model.access.csv',
        'data/awesome_estate_cron.xml',
        # Sample data (updates on -u; no noupdate so names reseed)
        'data/awesome_estate_demo.xml',
        'views/awesome_estate_property_views.xml',
        'views/awesome_estate_property_maintenance_views.xml',
        'views/awesome_estate_property_maintenance_subtask_views.xml',
        'views/awesome_estate_property_offer_views.xml',
        'views/awesome_estate_property_type_views.xml',
        'views/awesome_estate_property_tag_views.xml',
        'views/awesome_estate_res_users_views.xml',
        'views/awesome_estate_menus.xml',
    ],
    'application': True,
    'installable': True,
}
