
{
    'name': "Estate Account",
    'version': '1.0',
    'depends': ['base', 'estate', 'account'],
    'author': "Odoo S.A.",
    'category': 'Category',
    'description': "Description text",
    'website': 'https://www.odoo.com/page/estate',
    'license': 'LGPL-3',

    'data': [
        'security/ir.model.access.csv',
    
        'views/estate_account_menus.xml'
        
    ],
    'application': True,
    'installable': True
}
