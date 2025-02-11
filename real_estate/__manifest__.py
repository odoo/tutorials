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
        "security/ir.model.access.csv",
        "views/estate_properties_offer_views.xml",
        "views/estate_properties_views.xml",
        "views/estate_properties_type_views.xml",
        "views/estate_properties_tags_views.xml",
        "views/res_user_views.xml",
        "views/estate_properties_menus.xml",
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
        # 'demo/demo_data.xml',
    ],
}
