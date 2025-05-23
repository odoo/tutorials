{
    'name': 'estate',
    'version': '1.0',
    'sequence': 15,
    'summary': 'estate summary',
    'description': "",
    'depends': [
        'base'
    ],
    'data': [
        "views/estate_property_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_menus.xml",
        "security/ir.model.access.csv",
        "views/res_users_views.xml",
        "views/res_partner_views.xml"
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}
