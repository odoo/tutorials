{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base','mail'],
    'author': "Dhruv Godhani",
    'category': 'Real Estate/Brokerage',
    'description': """
    This is the first module
    """,
    # data files always loaded at installation
    'data': [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_res_user_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_menu.xml",
        "data/estate_property_type.xml"
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
        "demo/demo_data.xml"
    ],
    'application': True,
    'sequence': 1,
    'license': "LGPL-3"
}
