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
        'demo/demo_data.xml',
    ],
   
    'installable': True,
    'application': True,

}
