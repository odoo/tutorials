{
    'name': 'Estate',
    'category': 'Sales/Estate',

    'summary': 'Real Estate Management Module',
    'description': """
        This module is designed to manage real estate properties. 
        It allows users to store detailed information about properties, 
        such as name, description, price, living area, and more. 
        Users can also track the status of properties, availability, and other key details.
    """,
    'website': 'https://www.odoo.com/estate',
    'depends': [
        'base_setup',
    ],

    'data':[

        'security/ir.model.access.csv',
        'views/partner_salesman_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        'data/estate.property.type.csv'

    ],


    'demo':[
        'demo/estate_property.xml',
        'demo/estate_property_offer.xml'

    ],
    
    'application': True,
    'installable':True,
     'license': 'AGPL-3'


    
}