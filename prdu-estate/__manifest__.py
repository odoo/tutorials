{
    'name': "Estate module",
    'version': '0.1',
    'depends': ['base'],
    'author': "odoo.com",
    'category': 'Education',
    'description': """
    Lorem ipsum dolor sit amet
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'views/estateviews.xml',
        'views/estatemenus.xml',
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
    ],
    'installable': True,
    'application': True,
    'license': "LGPL-3"
}
