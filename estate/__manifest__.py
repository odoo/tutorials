{
    "name": "estate",
    "version": "1.0",
    "sequence": 1,
    "depends": ["base" , "mail"],
    "description": "This module is used to manage real estate properties.",
    "installable": True,
    "application": True, 
    "category": "Real Estate/Brokerage",
    'data' : [
            'security/security.xml',
            'security/ir.model.access.csv',
            'views/estate_property_views.xml',
            'views/estate_property_offer_views.xml',
            'views/estate_property_type_views.xml',
            'views/estate_property_tag_views.xml',
            'views/res_users_views.xml',
            'views/estate_menus.xml',
            'data/estate.property.type.csv',
            'report/estate_property_offer_template.xml',
            'report/estate_property_offer_subtemplate.xml',
            'report/estate_property_offer_res_user_template.xml',
            'report/estate_property_offer_reports.xml'
        ],
    'demo' : [
            'demo/estate_property.xml',
            'demo/estate_property_offer.xml'
    ],
    "license": "LGPL-3"
}
