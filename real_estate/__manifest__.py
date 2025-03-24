{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base','website'],
    'author': "Rishav Shah (sris)",
    'category': 'Real Estate/Brokerage',
    'icon':'/real_estate/static/src/img/real_estate_icon.png',
    'description': """    
        A module for managing real estate properties, including:
        - Property listings with various details.
        - Offers management with constraints and computed fields.
        - Property types and tags.
        - Security rules for user access.
      """,
    'installable':True,
    'application':True,
    'license':'LGPL-3',
    'data': [
        'security/estate_security.xml',
        'security/ir.model.access.csv',
        'views/estate_offer_wizard_view.xml',
        'report/estate_property_templates.xml',
        'report/res_user_template.xml',
        'report/estate_property_reports.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_views.xml',
        'views/res_users_views.xml',
        'views/estate_menus.xml',
        'views/website_property_template.xml',
    ],
    'demo': [
        'demo/res_user_demo.xml',
        'demo/estate_property_type_demo.xml',
        'demo/estate_property_tag_demo.xml',
        'demo/estate_property_demo.xml',
        'demo/estate_property_offer_demo.xml',
    ],
}
