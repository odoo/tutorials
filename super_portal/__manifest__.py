{
    'name': 'Super Portal User',
    'category': 'Portal',
    'summary': 'Portal access for multi-branch management',
    'depends': ['contacts', 'website_sale'],
    'data': [
        'security/portal_security.xml',
        'views/res_partner_views.xml',
        'views/portal_wizard_views.xml',
        'views/templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'super_portal/static/src/js/website_sale.js',
            'super_portal/static/src/js/address_search.js'
        ],
    },
    'license': 'LGPL-3',
    'installable': True,
}
