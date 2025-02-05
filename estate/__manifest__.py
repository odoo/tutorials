{
    'name': "Real Estate",
    'version': '1.0',
    # 'depends': ['base'],
    'author': "Dhruv Godhani",
    'category': 'Category',
    'description': """
    This is the first module
    """,
    # data files always loaded at installation
    'data': [
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_menu.xml"
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
    ],
    'application': True,
    'sequence': 1,
    'license': "LGPL-3"
}