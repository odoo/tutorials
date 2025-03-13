{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "Rishav Shah (sris)",
    'category': 'Estate',
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
        'security/ir.model.access.csv',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ],
    'demo': [
        'demo/res_user_demo.xml',
        'demo/estate_property_type_demo.xml',
        'demo/estate_property_tag_demo.xml',
        'demo/estate_property_demo.xml',
        'demo/estate_property_offer_demo.xml',
    ],
}
