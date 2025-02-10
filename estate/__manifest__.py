{
    'name': 'Real estate',
    'depends': ["base"],
    'data' : [
        "security/ir.model.access.csv",
        "views/estate_res_user_views.xml",
        "views/estate_property_offers_view.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_views.xml",
        "views/estate_menus.xml",
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3', 
}