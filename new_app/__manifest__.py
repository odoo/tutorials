{
    'name': 'My First App',
    'version': '1.0',
    'summary': 'A simple Odoo module',
    'sequence': 10,
    'description': 'This is my first custom Odoo module',
    'category': 'Custom',
    'author': 'Harsh Sharma',
    'license': 'LGPL-3',
    'depends': ['base'],  # This means it depends on the "base" module
    'data': [
        'security/ir.model.access.csv',  # Security rules
        'views/estate_property_views.xml', #UI views
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml'

    ],
    'installable': True,
    'application': True,
}
