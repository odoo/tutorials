{
    'name' : "Real Estate",

    'summary' : "A Real Estate Module that streamlines property listings, transactions, and client management with advanced search and analytics.",

    'description': """The Real Estate Module is a feature-rich solution for managing property listings, buyers, and transactions efficiently. It offers advanced search filters, virtual tours, and interactive maps to enhance the user experience. Built-in lead management and automated workflows help real estate professionals track inquiries and close deals faster. Secure document handling and analytics provide insights for better decision-making. Designed for agents, brokers, and property managers, this module ensures seamless real estate operations.""",

    'author': "Krunal Gelot",
    'website': "https://www.odoo.com",

    'category': 'Tutorials',
    'version': '0.1',

    'depends': ['base'],
    'application': True,
    'installable': True,

    'data' : [
        'security/ir.model.access.csv',
        'views/estate_property_offer_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_res_users_views.xml',
        'views/estate_menus.xml'
    ],

    'demo' : [
        'demo/demo_property.xml',
        'demo/demo_property_offer.xml',
        'demo/demo_property_tag.xml',
        'demo/demo_property_type.xml'
    ],

    'license': 'AGPL-3'
}
