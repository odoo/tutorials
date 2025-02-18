{
    "name": "Real Estate",
    'category': 'Real Estate/Brokerage',
    'depends': ['base','mail','website'],
    "data": [
            "security/security.xml",
            "security/ir.model.access.csv",
            "views/estate_property_views.xml",
            "views/estate_property_offer_views.xml",
            "views/estate_property_type_views.xml",
            "views/estate_property_tag_views.xml",
            "report/estate_property_reports.xml",
            "report/estate_property_templates.xml",
            "report/estate_property_salseman_report.xml",
            "views/estate_properties_detail.xml",
            "views/estate_properties_template.xml",
            "views/inherit_model_views.xml",
            "views/estate_menus.xml",
    ],
    "demo": [
        "demo/estate_property_type_demo.xml",
        "demo/estate_property_tag_demo.xml",
        "demo/estate_property_demo.xml",
        "demo/estate_property_offer_demo.xml",
    ],
    'installable': True,
    "application": True,
    "license": "LGPL-3"
}
