{
    'name': 'Estate',
    'version': '1.1',
    'category': 'Tutorials',
    'summary': 'The Real Estate Advertisement module',
    'description': 'Try installing the App',
    'depends': ['base', 'mail'],
    'application': True,
    'installable': True,
    'author': 'times',
    'website': 'https://www.odoo.com/app/estate',
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'report/estate_property_report.xml',
        'data/estate_property_mail_template.xml',
        'views/estate_property_views.xml',
        'views/estate_property_offer.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_dashboard_views.xml',
        'views/res_users_views.xml',
        'views/estate_menus.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'estate/static/src/components/**/*',
            'estate/static/src/scss/estate_form.scss',
            'estate/static/src/components/price_tag_widget/estate_price_tag_widget.js',
            'estate/static/src/components/price_tag_widget/estate_price_tag_widget.xml',
            'estate/static/src/components/price_tag_widget/estate_price_tag_widget.scss',
        ],
        'estate.dashboard': [
            'estate/static/src/components/estate_dashboard/**/*',
        ]
    },
}
