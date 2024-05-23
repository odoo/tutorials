{
    "name": "estate",
    "version": "1.0",
    "depends": ["base"],
    "author": "odoo dev",
    "category": "Category",
    "installable": True,
    "application": True,
    "license": "LGPL-3",
    "description": """
    Description text
    """,
    # # data files always loaded at installation
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_menu.xml",
    ],
    # # data files containing optionally loaded demonstration data
    # 'demo': [
    #     'demo/demo_data.xml',
    # ],
}
