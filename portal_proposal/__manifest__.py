{
    'name': "portal-proposal",
    'version': "1.0",
    'depends': ["base", "sale", "sale_management"],
    'author': "Dhruv",
    'category': "Tutorials/PortalProposal",
    'application': True,
    'installable': True,
    'description': """
    Module for Portal Proposal
    """,
    'data': [
        'security/ir.model.access.csv',
        'views/sale_proposal_views.xml',
        'views/inherit_sale_menus.xml',
        'views/proposal_portal_templates.xml',
    ],
    'demo': [],
    'license': 'AGPL-3',
}
