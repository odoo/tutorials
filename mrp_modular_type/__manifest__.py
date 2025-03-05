{
    'name': 'Custom MRP Modular Type',
    'version': '1.0',
    'category': 'Manufacturing',
    'author': 'Vaidik Gorasiya',
    'depends': ['sale_management', 'mrp'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_views.xml',
    ],
    'installable': True,
}
