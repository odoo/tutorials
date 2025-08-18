{
    'name': 'Real Estate',
    'category': 'Real Estate/Brokerage',
    'application': True,
    'installable': True,
    'depends': ['base'],
    'data': [
        'security/estate_security.xml',
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ],
	'license': 'LGPL-3',
}
