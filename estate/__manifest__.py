{
    'name': "Estate",
    'license': 'LGPL-3',
    'depends': [
        'base',
    ],
    'data': [
        'reports/estate_property_report.xml',
        'reports/estate_property_report_template.xml',
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/inherited_user_views.xml',
        'views/estate_menus.xml',
        'data/estate.property.type.csv',
        'demo/demo_property.xml',
        'demo/demo_property_offer.xml',
    ],
    'installable': True,
    'application': True,
}
