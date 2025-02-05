{
    'name': "Real Estate Module",

    'summary': "Starting module for Real Estate Project",
    'description': "Starting module for Real Estate Project Description",

    'author': "Odoo SA",
    'website': "https://www.odoo.com/",
    'category': 'Tutorials',
    'version': '1.0',
    'application': True,
    'installable': True,
    'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_views_list.xml',
        'views/estate_property_views_form.xml',
        'views/estate_menu_views.xml'
    ],
    'license': 'AGPL-3'
}
