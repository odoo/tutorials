{
    "name": "Portal Proposal",
    "version": "1.0",
    "summary": "Portal Proposal",
    'depends': ['base', 'portal', 'sale_management'],
    "data": [
        "security/ir.model.access.csv",
        "security/security.xml",
        "views/email_template_sale_proposal.xml",
        "views/sale_proposal_portal_template.xml",
        "views/proposal_views.xml",
        "views/proposal_menus.xml",
    ],
    "installable": True,
    "application": True,
    "license": "AGPL-3",
}
