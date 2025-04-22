{
    'name': 'Real Estate',
    'version': '1.0',
    'category': 'Real Estate Sales Management',
    'author': 'UMBM',
    'summary': 'Manage appartments rent',
    'description': "",
    'license': "GPL-3",
    'website': 'https://www.odoo.com/page/crm',
    'depends': [
        'base',
    ],
    'data': [
        './security/ir.model.access.csv',
        './views/estate_property_views.xml',
    ],
    'demo': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False
}