{
    'name': 'Odoo Tutorial Real Estate',
    'category': 'Real Estate',
    'version': '19.0.1.0',
    'author': 'Hazei',
    'license': 'LGPL-3',
    'summary': 'Real Estate Management Tutorial',
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type.xml',
        'views/estate_property_tags_view.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
}
