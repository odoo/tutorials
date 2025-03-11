{
    'name' : "Real Estate",
    'summary' : "A Real Estate Module that streamlines property listings, transactions, and client management with advanced search and analytics.",
    'description': """
        The Real Estate Module is a feature-rich solution for managing property listings,
        buyers, and transactions efficiently. It offers advanced search filters,
        virtual tours, and interactive maps to enhance the user experience.
        Built-in lead management and automated workflows help real estate professionals track inquiries and close deals faster.
        Secure document handling and analytics provide insights for better decision-making. Designed for agents, brokers,
        and property managers, this module ensures seamless real estate operations.
    """,
    'icon': '/estate/static/description/icon.png',
    'author': "Krunal Gelot",
    'website': "https://www.odoo.com",
    'category': 'Real Estate/Brokerage',
    'version': '0.1',
    'depends': ['base', 'website', 'mail'],
    'application': True,
    'installable': True,
    'data' : [
        'views/res_config_settings_views.xml',
        'views/estate_property_templete.xml',
        'security/group_security.xml',
        'security/ir.model.access.csv',
        'views/estate_property_offer_views.xml',
        'wizard/estate_property_multiple_offer_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_res_users_views.xml',
        'security/estate_security.xml',
        'report/estate_property_templates.xml',
        'report/estate_property_reports.xml',
        'views/estate_menus.xml'
    ],
    'demo' : [
        'demo/demo_property_type.xml',
        'demo/demo_property_tag.xml',
        'demo/demo_property.xml',
        'demo/demo_property_offer.xml'
    ],
    'license': 'AGPL-3'
}
