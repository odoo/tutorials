{
    'name': "Real Estate",
    'summary': "This is the real estate module that is used for buying and selling propertise!!",
    'description': "This is the real estate module that is used for buying and selling propertise!!",
    'version': '0.1',
    'application': True,
    'category': 'Tutorials',
    'installable': True,
    'depends': ['base'],
    'data': [
        "security/ir.model.access.csv",
        "views/estate_property_view.xml",
        "views/estate_property_type_view.xml",
        "views/estate_property_tag_view.xml",
        "views/estate_property_offer.xml",
        "views/estate_menus.xml",
    ],
    'license': 'AGPL-3'
}
