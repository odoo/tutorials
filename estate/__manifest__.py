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
        'views/estate_property_view.xml',
        'views/estate_property_offer_view.xml',
        'views/estate_property_type_view.xml',
        'views/estate_property_tags_view.xml',
        'views/estate_property_menu_view.xml',
        'views/users_properties.xml'

    ],
    
    'application': True,
    'installable':True,
     'license': 'AGPL-3'


    
}