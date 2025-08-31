{
    'name': 'Packaging Controll',
    'version': '1.0',
    'summary': 'Controll of packaging procces, for furniture production',
    'category': 'Manufacturing',
    'author': 'Nikita Brazhnikov',
    'depends': ['base', 'mrp', 'stock', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/packaging_views.xml',
    ],
    'installable': True,
    'application': True, 
}