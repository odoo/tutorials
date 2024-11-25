{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base'],
    'category': 'Training',

    'data': [
        'security/estate_groups.xml',
        'security/ir.model.access.csv',
        'security/estate_security.xml',

        # views
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/res_users_views.xml',

        # reports
        'report/estate_property_templates.xml',
        'report/estate_property_reports.xml',
        'report/res_users_templates.xml',
        'report/res_users_reports.xml',

        # menu
        'views/estate_menus.xml',

        # data
        'data/estate.property.type.csv',

    ],
    'demo': [
        'demo/estate_property.xml',
        'demo/estate_property_offer.xml',
    ],
    'application': True,
    'license': 'AGPL-3',
}
