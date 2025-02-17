{
    'name': 'Real estate',
    'application': True,
    'category': 'Real Estate/Brokerage',
    "depends" : ['base','mail','website'],
    "data": [
            "security/estate_security.xml",
            "security/ir.model.access.csv",
             "views/estate_property_views.xml",
             "views/estate_property_offer_views.xml",
             "views/estate_property_type_views.xml",
             "views/estate_property_tag_views.xml",
             "views/res_users.xml",
             "views/estate_menus.xml",
             "views/estate_properties_template.xml",
             "views/estate_property_details.xml"
             ],
    "demo": [
            "demo/estate_property_type_demo.xml",
            "demo/estate_property_tag_demo.xml",
            "demo/estate_property_demo.xml",
            "demo/estate_property_offer_demo.xml",
        ],
        'assets': {
        'web.assets_backend': [
            'estate/static/description/icon.png',
        ],
    },
    'images': ['static/description/icon.png'],
    "license": "LGPL-3",
    "installable":True
}
