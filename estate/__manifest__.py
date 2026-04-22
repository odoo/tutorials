{
    'name': 'Estate',
    'version': '19.0.1.1.0',
    'depends': [
        'base',
    ],
    'author': 'Stef Ossé',
    'license': 'LGPL-3',
    'category': 'Category',
    'description': '''
    A specialized application for **estate management**.
    ''',
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_menus.xml',
    ],
    # data files containing optionally loaded demonstration data
    'demo': [],
    'application': True
}
