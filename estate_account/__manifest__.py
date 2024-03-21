{
    'name': 'Estate Account',
    'version': '1.0',
    'category': 'Tutorials/Estate',
    'summary': 'Real Estate Account',
    'author': 'Muhamed Abdalla (muab)',
    'description':
    """
    Responsible on invoicing the buyer of the estate properties
    """,
    'website': "https://www.odoo.com",
    'depends': [
        'base',
        'estate',
        'account'
    ],
    'data': [
        'security/ir.model.access.csv'
    ],
    'application': True,
    'license': 'AGPL-3'
}
