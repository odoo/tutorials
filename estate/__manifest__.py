{
    "name": "Real Estate",
    "category": "Real Estate/Brokerage",
    "depends":["base","mail","website"],
    "data": [
            "security/security.xml",
            "security/ir.model.access.csv",
            "views/estate_property_views.xml",
            "views/estate_property_offer.xml",
            "views/estate_property_type.xml",
            "views/estate_property_tag.xml",
            "views/inherited_model.xml",
            'views/estate_properties_template.xml',
            'views/estate_properties_details.xml',
            "views/estate_menus.xml",
            "report/estate_property_reports.xml",
            "report/estate_property_report_template.xml",
            "report/estate_property_salesman_report.xml"
    ],
    'demo': [
        "demo/estate_property_type_demo.xml",
        "demo/estate_property_tag_demo.xml",
        "demo/estate_property_demo.xml",
        "demo/estate_property_offer_demo.xml",
    ],
    'assets': {
        'web.assets_backend': [
            'estate/static/description/icon.png',
        ],
    },
    'images': ['static/description/icon.png'],
    "installable": True,
    "application": True,
    "license": "LGPL-3"
}
