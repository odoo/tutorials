{
    'name': 'Real Estate',
    'version': '1.0',
    'summary': 'Real Estate Management Module',
    'author': 'chirag Gami(chga)',
    'category': 'Brokerage',
    'depends': ['base'],
    'license':'LGPL-3',
    'data': [
        # Add your XML/CSV files if any
        'security/ir.model.access.csv',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ],
    'demo': [
        'demo/estate_res_partner_demo.xml',
        'demo/estate_property_tag_demo.xml',
        'demo/estate_property_type_demo.xml',
        'demo/estate_property_demo.xml',
        'demo/estate_property_offer_demo.xml',
    ],
    'installable': True,  # This is required!
    'application': True,
}
