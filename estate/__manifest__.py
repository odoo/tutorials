{
    'name': 'Real Estate',
    'version': '1.0',
    'category': 'Real Estate',
    'summary': 'Module for managing real estate properties.',
    'author': 'Your Name',
    'depends': ['base'],
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'wizard/estate_add_offer_wizard_view.xml',
        'view/estate_property_offer_view.xml',
        'view/estate_property_views.xml',
        'view/estate_property_type_view.xml',
        'view/estate_property_tag_view.xml',
        'view/res_users_view.xml',
        'view/estate_menus.xml',
        'data/property_type.xml'
    ],
    'demo': [
        'demo/estate_property_demo.xml',
        'demo/estate_demo_offers.xml'
    ],
    'installable': True,
    'application': True,
}
