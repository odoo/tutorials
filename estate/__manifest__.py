{
    'name': 'Real Estate',
    'version': '1.0',
    'description': 'Real Estate Management System',
    'summary': 'Real Estate Management System',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_offer.xml',
        'views/estate_property_tag.xml',
        'views/estate_property_type.xml',
        'views/estate_property.xml',
        'views/estate_menus.xml',
        'views/res_user.xml',
        'data/estate.property.type.csv',
    ],
    'demo': [
        'demo/estate_property.xml',
        'demo/estate_property_offer.xml',
    ],
    'auto_install': False,
    'application': True,
}
