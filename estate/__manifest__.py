{
    'name': "Real Estate",
    'version': "1.0",
    'depends': ["base"],
    'author': "lotr following Odoo tutos",
    'category': "Category",
    'description': """
    Description text
    """,
    'installable': True,
    'application': True,
    'license': "LGPL-3",
    # data files always loaded at installation
    'data': [
        "security/ir.model.access.csv",
        "views/estate_property.xml",
        "views/estate_property_offers.xml",
        "views/estate_property_type.xml",
        "views/estate_property_tag.xml",
        "views/estate_property_menus.xml",
        "views/estate_users.xml",
    ],
    # # data files containing optionally loaded demonstration data
    # 'demo': [
    #     'demo/demo_data.xml',
    # ],
}
