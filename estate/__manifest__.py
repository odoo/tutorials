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
    'category': 'Tutorials/Estate',
    'version': '0.1',

    'data':[
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_type_views.xml',      
        'views/estate_menus.xml'
    ],

    'installable':True,
    'application':True,
    'license': "LGPL-3" 
    
}
