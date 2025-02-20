{
    'name': 'Real Estate',
    # 'version': '1.2',
    'category': 'Real Estate/Brokerage',
    # 'sequence': 15,
    # 'summary': 'cover a business area',
    # 'description': "",
    # 'website': 'https://www.odoo.com/page/crm',
    'depends': [
        'base',
        'mail',
        'whatsapp',
        'website',
    ],
    'data': [
         'report/estate_property_report.xml',
         'report/estate_property_templates.xml',
         'report/estate_user_properties_report.xml',
         'report/estate_user_properties_templates.xml',

         'security/estate_property_security.xml',
         'security/ir.model.access.csv',

         'data/master_data.xml',
         'data/estate_property_email_template.xml',

         'wizard/estate_property_offer_wizard_views.xml',

         'views/estate_property_details_website.xml',
         'views/estate_property_website.xml',
         'views/estate_property_offer_views.xml',
         'views/estate_property_views.xml',
         'views/estate_property_type_views.xml',
         'views/estate_property_tag_views.xml',
         'views/res_users_views.xml',
         'views/estate_property_menus.xml',
         'views/website_menu.xml',
    ],
    'demo' : [
        'demo/estate_property_demo.xml',
    ],
   
    'installable': True,
    'application': True,

}
