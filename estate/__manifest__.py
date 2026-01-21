{
    'name': 'Real Estate',
    'category': 'tutorials',
    'summary': 'Real estate module to sell/rent houses and offices',
    'description': """
    immoweb alias xd
    """,
    'website': 'https://www.odoo.com/app/real_estate',
    'depends': [
        'base_setup',
        'base'
    ],
    'data': [
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
    'author': 'ibrha',
    'license': 'LGPL-3',
}