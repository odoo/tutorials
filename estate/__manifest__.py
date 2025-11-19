{
    'name': 'Real Estate',
    'description': 'Real Estate !',
    'version': '1.0',
    'summary': 'Track Real Estate',
    'website': 'https://www.odoo.com/app/realestate',
    'author': 'Odoo S.A.',
    'application': True,
    'license': 'LGPL-3',
    'depends': [
        'base',
    ],
     'data': [
         'security/ir.model.access.csv',
         'views/estate_property_views.xml',
         'views/estate_menus.xml',
     ],
}
