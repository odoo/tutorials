# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'CRM contact details',
    'version': '1.0',
    'depends': ['crm'],
    'description': """
It provides crm contact details
""",
    'data': [
        'views/crm_lead_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'crm_contact_details/static/src/many2many_unlink/*',
        ],
    },
    'installable': True,
    'license': 'LGPL-3',
}
