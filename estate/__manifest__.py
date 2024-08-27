{
    'name': 'estate',
    'version': '1.0',
    'summary': 'An real state management application',
    'description': 'A detailed description of my module',
    'category': 'Sales',
    'author': 'prgo',
    'depends': ['base'],
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'wizard/add_offer_wizard_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_types_views.xml',
        'views/estate_property_tags_views.xml',
        'views/estate_property_offers_views.xml',
        'views/res_users_views.xml',
        'views/estate_menus.xml'
    ],
    'installable': True,
    'application': True,
}
