{
    'name': 'Estate Account',
    'summary': 'Invoice property buyers',
    'description': """
        Link between real estate management and accounting by invoicing property buyers as part of the "Sever framework 101" tutorial
    """,
    'author': 'Odoo',
    'website': 'https://www.odoo.com',
    'version': '0.1',
    'application': True,
    'installable': True,
    'depends': ['estate', 'account'],
    'data': [
        'security/ir.model.access.csv',
    ],
    'license': 'AGPL-3',
}
