{
    'name': 'ESTATE',
    'version': '1.2',
    'description': "",
    'depends': [
        'base_setup',
    ],
    'data': [
        'security/ir.model.access.csv',

        'data/estate_property_type_data.xml',

        'wizard/estate_property_offer_wizard_view.xml',

        'report/estate_property_offers_report_template.xml',
        'report/estate_property_offers_report.xml',
        'views/estate_property_views.xml',
        'views/estate_property_menu.xml',
        'views/estate_property_offer_view.xml',
        'views/estate_property_type_view.xml',
        'views/estate_property_type_menu.xml',
        'views/estate_property_tag_view.xml',
        'views/estate_property_tag_menu.xml',
        'views/res_users_view.xml'
    ],
    'demo': [
        'data/estate_property_demo.xml',
        'data/estate_property_offers_demo.xml'
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3'
}
