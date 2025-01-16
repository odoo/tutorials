{
    'name': 'Estate',
    'category': 'Real Estate/Brokerage',
    'summary': 'Real Estate Management Module',
    'description': """
        This module is designed to manage real estate properties. 
        It allows users to store detailed information about properties, 
        such as name, description, price, living area, and more. 
        Users can also track the status of properties, availability, and other key details.
    """,
    'depends': [
        'base', 'website'
    ],
    'data':[
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/partner_salesman_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        'views/estate_property_website_templates.xml',
        'data/estate.property.type.csv',
        'report/estate_property_templates.xml',
        'report/estate_property_reports.xml',
        'wizard/estate_property_make_bulk_offer.xml',
    ],
    'demo':[
        'demo/estate_property.xml',
        'demo/estate_property_offer.xml'
    ],
    'application': True,
    'installable':True,
    'auto_install':True,
    'license': 'LGPL-3',
}
