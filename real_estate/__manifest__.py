{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base'],
    'icon': '/real_estate/static/description/estate_icon.png',
    'author': "Krishna Pathak",
    'category': 'Category',
    'description': """
    This is descritption text
    """,
    # data files always loaded at installation
    'data': [
        # 'views/mymodule_view.xml',
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_menus.xml"
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
        # 'demo/demo_data.xml',
    ],
}