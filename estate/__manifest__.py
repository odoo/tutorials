{
    'name': "Real Estate",
    'summary': "This is the real estate module that is used for buying and selling propertise!!",
    'description': "This is the real estate module that is used for buying and selling propertise!!",
    'version': '0.1',
    'application': True,
    'category': 'Real Estate/Brokerage',
    'installable': True,
    'depends': ['base','mail'],
    'data': [
        "report/estate_property_reports.xml",
        "report/estate_property_templates.xml",
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/estate_property_view.xml",
        "views/estate_property_offer.xml",
        "views/estate_property_type_view.xml",
        "views/estate_property_tag_view.xml",
        "views/ir_cron.xml",
        "views/res_user_view.xml",
        "views/estate_menus.xml",
        "data/estate_property_types.xml",
        "demo/estate_property_demo.xml",
        "demo/estate_property_offer_demo.xml"
    ],
    'license': 'AGPL-3'
}
