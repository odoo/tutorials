{
    'name': "Real Estate",
    'summary': "Manage real estate assets",
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'actions.xml',
        'ir.model.access.csv',
        'menus.xml',  # Depends on `actions.xml`
        'real_estate_property_data.xml',
    ],
    'application': True,
}
