{
    'name': 'Esate By Akpu',
    'Description': "Starting module for Estate",
    'license': 'LGPL-3',
    'summary': "Starting module for Real Estate Business model",
    'author': 'Akpu_odoo',
    'version': '0.1',
    'application': True,
    'installable': True,
    'depends': ['base','mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        'views/list_model_view.xml',
    ],
}
