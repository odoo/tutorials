{
    'name': 'My Real Estate',
    'license': 'LGPL-3',
    'icon': '/real_estate/static/src/images/real-estate-icon.png',
    'depends': ['base'],
    'installable': True,
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'report/real_estate_property_offer_templates.xml',
        'report/real_estate_property_offer_reports.xml',
        'views/real_estate_property_views.xml',
        'views/real_estate_property_offers_views.xml',
        'views/real_estate_property_category_views.xml',
        'views/real_estate_property_tags_views.xml',
        'views/res_user.xml',
        'views/real_estate_menus.xml',
        'report/user_property_templates.xml',
        'report/user_property_reports.xml',
    ],
    'demo': [
        'demo/demo_real_estate_partner.xml',
        'demo/demo_real_estate_property_category.xml',
        'demo/demo_real_estate_property_tag.xml',
        'demo/demo_real_estate_property.xml',
        'demo/demo_real_estate_property_offer.xml',
    ]
}
