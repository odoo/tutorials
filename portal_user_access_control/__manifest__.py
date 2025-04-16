{
    'name': "Portal user access control",
    'summary': "Control what portal user can see",
    'depends': ['project', 'portal', 'website', 'contacts', 'sale', 'purchase', 'account'],
    'data': [
        'security/security.xml',
        'views/res_user_views.xml',
        'wizard/portal_wizard_views.xml',
        'views/portal_templates.xml',
    ],
    'installable': True,
    "license": "LGPL-3"
}
