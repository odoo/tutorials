{
    'name': "Real Estate",
    'summary': "Manage real estate assets",
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        # Model data
        'data/res_partner_data.xml',
        'data/real_estate_property_type_data.xml',
        # Depends on `res_partner_data.xml`, `real_estate_property_type_data.xml`
        'data/real_estate_property_data.xml',

        # Security
        'security/ir.model.access.csv',

        # Views
        'views/real_estate_offer_views.xml',
        'views/real_estate_property_type_views.xml',
        'views/real_estate_property_views.xml',
        'views/menus.xml',  # Depends on actions in views.
    ],
    'application': True,
}
