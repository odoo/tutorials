{
    'name':"estate",
    'author':"Odoo S.A.",
    'licence':"none",
    
    'summary': """
        Houses!
    """,

    'description': """
        Lots of Houses!!"
    """,
    
    'application': True,
    'installable': True,
    'data':[
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_types_views.xml',
        'views/estate_property_tags_views.xml',
        'views/estate_property_offers_views.xml',
        'views/estate_menus.xml',
        'views/estate_users.xml',
    ],
}
