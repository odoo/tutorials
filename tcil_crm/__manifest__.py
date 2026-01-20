# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    "name": "TCIL CRM",
    "version": "18.0.1.0.0",
    "license": "LGPL-3",
    "author": "Odoo PS",
    "category": "Custom Development",
    "website": "https://www.odoo.com",
    "depends": ["crm", "contacts"],
    "summary": "TCIL CRM",
    "description": """
        - Created a field in CRM Stage, Crm Lead and a new page 'Service Vertical' in CRM Lead form view.

        - Manage the Address Details and the Contact Details on the Opportunity Form.
    """,
    "data": [
        "views/crm_stage_views.xml",
        "views/crm_lead_views.xml",
    ],
    'assets': {
        'web.assets_backend': [
            'tcil_crm/static/src/scss/hide_x2many_remove_button.scss',
        ],
    },
    "installable": True,
}
