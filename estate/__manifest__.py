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
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}
