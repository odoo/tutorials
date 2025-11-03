{
    'name': "Estate",
    'category': "Real Estate/Brokerage",
    'depends': [
        'base'
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/estate.property.type.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/res_user_view.xml',
        'views/estate_menus.xml',
    ],
    "demo": [
        'demo/demo_data.xml'
    ],
    'application': True,
    'author': "Odoo S.A.",
    'license': "LGPL-3",
}
