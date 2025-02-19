{
    'name': 'Real Estate',
    'version': '1.0',
    'depends': ['base', 'mail', 'rating'],
    'author': 'ATPA',
    'category': 'Real Estate/Brokerage',
    'description': """
Real Estate module is for training, the module contains property types, offers and tags.
""",
    'data' : [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/estate_property_sequence.xml',
        'data/mail_message_subtype.xml',
        'data/estate_rating_email_template.xml',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/res_users_view.xml',
        'views/estate_property_menus.xml',
        'views/rating_rating_view.xml',
    ],
    'demo' : [
        'demo/estate_property_type_demo.xml',
        'demo/estate_property_demo.xml',
        'demo/estate_property_offer_demo.xml',
    ],
    'application' : True,
    'license' : 'LGPL-3' 
}
