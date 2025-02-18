{
    'name': "Estate",
    'description': """
        It is an application made for users for a purchase and sales
        of there properties and make experience smoother
        """,
    'sequence': 1,
    'depends': ["base","website","mail"],
    'category': "Real Estate/Brokerage",
    'data': [
        "security/security.xml",
        "security/ir.model.access.csv",
        "report/estate_property_reports.xml",
        "report/estate_property_templates.xml",
        "views/estate_property_list.xml",
        "views/estate_property_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_offer_views.xml",
        "views/res_users_view.xml",
        "views/estate_menus.xml"
    ],
    'demo': [
        "demo/estate_property_demo.xml",
    "demo/estate_property_type_demo.xml",
    "demo/estate_propert_offer_demo.xml"
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
