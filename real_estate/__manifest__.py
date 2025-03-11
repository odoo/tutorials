{
    'name': "My Real Estate",
    'license': 'LGPL-3',
    'depends': ['base'],
    'installable': True,
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'views/real_estate_property_views.xml',
        'views/real_estate_property_offers_views.xml',
        'views/real_estate_property_category_views.xml',
        'views/real_estate_property_tags_views.xml',
        'views/real_estate_menus.xml',
    ],
    'demo': [
        'demo/demo_real_estate_partner.xml',
        'demo/demo_real_estate_property_category.xml',
        'demo/demo_real_estate_property_tag.xml',
        'demo/demo_real_estate_property.xml',
        'demo/demo_real_estate_property_offer.xml',
    ]
}
