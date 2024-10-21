{
    'name': "Real Estate",
    'version': '0.1',
    'depends': ['base'],
    'description': "A real estate app",
    'category': 'Tutorials/RealEstate',
    'application': True,
    # data files always loaded at installation
    'data': [
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/res_users_views.xml",
        "views/estate_menus.xml"
    ],
    'license': "LGPL-3",
    'demo': [
        "data/estate_property_demo.xml",
    ],
}
