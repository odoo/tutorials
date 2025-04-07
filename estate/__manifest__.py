{
    'name': 'Real Estate',
    'description': 'Buy and sell Real Estate properties',
    'category': 'Real Estate/Brokerage',
    'license': 'GPL-3',
    'depends': [
        'base',
        'website'
    ],
    'data': [
        'security/estate_security.xml',
        'security/ir.model.access.csv',
        'data/estate.property.type.csv',
        'wizard/estate_property_bulk_offers_view.xml',
        'views/estate_property_views.xml',
        'views/estate_property_offers_view.xml',
        'views/estate_property_tag_view.xml',
        'views/estate_property_types_view.xml',
        'report/estate_property_templates.xml',
        'report/estate_property_reports.xml',
        'views/res_users_view.xml',
        'views/estate_menus.xml',
        'data/website_menus.xml',
    ],
    'demo': [
        'demo/estate_property_demo.xml',
        'demo/estate_property_offer_demo.xml'
    ],
    'installable': True,
    'application': True
}
