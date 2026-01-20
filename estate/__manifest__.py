{
    'name': 'Real Estate',
    'category': 'Sales',
    'description': 'Advertise your real estate',
    'author': '[THDES] Thomas des Touches',
    'depends': [
        'base_setup',
    ],
    'application': True,
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menu_views.xml',
    ],
}
