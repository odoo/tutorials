{
    'name': 'Real Estate',
    # 'version': '1.2',
    # 'category': 'Real Estate',
    # 'sequence': 15,
    # 'summary': 'cover a business area',
    # 'description': "",
    # 'website': 'https://www.odoo.com/page/crm',
    'depends': [
        'base',
    ],
    'data': [
         'security/ir.model.access.csv',
         'views/estate_property_views.xml',
         'views/estate_property_type_views.xml',
         'views/estate_property_tag_views.xml',
         'views/estate_property_offer_views.xml',
         'views/inherited_user_views.xml',
         'views/estate_menus.xml',

    ],
   
    'installable': True,
    'application': True,
}

