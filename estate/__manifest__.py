{
    'name': "tuto_estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "Dahen",
    'license': "LGPL-3",
    'category': 'Sales',
    'description': """
    Description text
    """,
    # data files always loaded at installation
    'data': [
        "security/ir.access.csv",
        "views/estate_property_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_menu_views.xml"
    ],
    'application': True,
}
