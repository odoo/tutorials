{
    'name': "Sevan Estate",
    'depends': ['base'],
    'summary': "Just a simple estate app for Sevan.",
    'application': True,
    'installable': True,

    'data': [
        'security/ir.model.access.csv',

        # Be careful with the order!
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_menus.xml',
    ],
    'author': "Sevan Corp.",
}
