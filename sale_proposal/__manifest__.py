{
    'name': 'Sale Proposal',
    'version': '1.0',
    'summary': 'Manage sales proposals with customer interaction',
    'description': 'A module to manage proposals that customers can view and edit online.',
    'author': 'NIAD',
    'category': 'Sales',
    'depends': ['base', 'sale', 'portal', 'sale_management', 'website'],
    'data': [
        "security/security.xml",
        "security/ir.model.access.csv",
        'views/sale_proposal_views.xml',
        'views/portal_sale_proposal_template.xml',
    ],
    'application': True,
}
