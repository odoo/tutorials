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
    ],
    'data': [
         'report/estate_property_report.xml',
         'report/estate_property_templates.xml',
         'report/estate_user_properties_report.xml',
         'report/estate_user_properties_templates.xml',
         'security/estate_property_security.xml',
         'security/ir.model.access.csv',
         'views/estate_property_offer_views.xml',
         'views/estate_property_views.xml',
         'views/estate_property_type_views.xml',
         'views/estate_property_tag_views.xml',
         'views/res_users_views.xml',
         'views/estate_property_menus.xml',
         'data/master_data.xml',
    ],
    'demo' : [
        'demo/estate_property_demo.xml',
    ],
   
    'installable': True,
    'application': True,

}
