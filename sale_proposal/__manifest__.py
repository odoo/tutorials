{
    'name': "Sale Proposal",
    'version': '1.0',
    'depends': ['base', 'sale_management', 'sale', 'website'],
    'author': "Vansh",
    'category': 'Sale Management',
    'description': """Find Your sale Here""",
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/sale_proposal_views.xml',
        'views/sale_menu.xml',
        'views/templates.xml',
    ],
    "demo": [
    ],
    'installable': True,
    "application": True,
    'license': "AGPL-3",
}
