{
    'name': "Estate",
    'summary': """
        Estate Made Easy
    """,

    'description': """
        Estate can be very easy with Odoo
    """,

    'author': "Odoo",
    'website': "https://www.odoo.com",
    'category': 'Real Estate/Brokerage',
    'version': '0.1',

    'depends': [
        'base',
        'web',
        'website'
    ],

    'data':[
        'security/estate_groups.xml',
        'security/estate_security.xml',
        'security/ir.model.access.csv',
        'wizard/estate_property_offer_wizard_views.xml',
        'report/estate_property_report_templates.xml',
        'report/estate_property_reports.xml',
        'views/estate_property_template.xml',
        'views/estate_property_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/res_user_views.xml',
        'views/estate_menus.xml'
    ],

    'demo':[
        'data/estate_property_type_data.xml',
        'data/estate_property_data.xml',
        'data/estate_property_offer_data.xml',
        'data/estate_property_tag_data.xml'
    ],

    'installable':True,
    'application':True,
    'license': "LGPL-3"
}
