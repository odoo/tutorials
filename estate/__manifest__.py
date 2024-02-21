{
    'name': 'Real Estate',
    'version': '1.0',
    'summary': "Real Estate Advertisement",
    'description': 'This is the real estate advertisement app which is a part of the odoo technical training',
    'depends': [
        'base'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menus.xml',
    ],
    'application': True
}
