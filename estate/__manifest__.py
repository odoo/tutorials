{
    'name': 'Real Estate',
    'version': '1.0',
    'summary': 'Real Estate Management Module',
    'author': 'Your Name',
    'category': 'Sales',
    'depends': ['base'],
    'license':'LGPL-3',
    'data': [
        # Add your XML/CSV files if any
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_menus.xml',
    ],
    'installable': True,  # This is required!
    'application': True,
    'auto-install': False,
}
