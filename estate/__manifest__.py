{
    'name': "estate",
    'version': '0.1',
    'depends': ['base_setup'],
    'description': "Technical practice",
    'installable': True,
    'application': True,

     'data': [
         'security/ir.model.access.csv',
         'views/estate_property_views.xml',
         'views/estate_property_type.xml',
         'views/estate_property_tag_view.xml',
         'views/estate_property_offer_view.xml',
         'views/estate_menus.xml',
             ],
    'license': 'LGPL-3',
}
