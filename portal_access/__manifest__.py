# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Portal Access Control",
    'version': '1.0',
    'category': "Hidden",
    'description': """
        Define access control for portal users.
    """,
    'depends': ['portal', 'sale_management', 'purchase', 'project'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/portal_wizard_views.xml',
        'views/res_users_views.xml',
        'views/portal_templates.xml'
    ],
    'installable': True,
    'license': "LGPL-3",
}
