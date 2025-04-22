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
        #'./views/real_estate_view.xml',
    ],
    'demo': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False
}