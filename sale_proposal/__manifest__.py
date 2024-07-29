{
    'name': "sale Proposal",
    'version': '1.0',
    'depends': ['base', 'sale', 'sale_management', 'website'],
    'author': "GAJA",
    'category': 'Sales/Sales',
    'description': """
    Hell Hoo
    """,
    'data': [
        'security/ir.model.access.csv',
        'views/sale_proposal_order.xml',
        'views/sale_proposal_views.xml',
        'views/sale_proposal_menus.xml',
        'views/sale_portal_template.xml',
    ],
    'demo': [],
    'application': True,

    'license': 'AGPL-3',
}
