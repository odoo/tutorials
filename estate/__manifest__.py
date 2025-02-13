{
    'name':"Real Estate", # this will be the user friendly name of the module will show as the name of our moudle 

    'summary':"an application which helps every real estate business owner", 

    'description':"This application is designed to streamline operations for real estate business owners, offering a comprehensive platform to manage property listings, client interactions, and transactions efficiently. ",

    'author': "panj",
    'website': "https://www.odoo.com",

    'category': 'Tutorials/RealEstate',

    'version': '0.1',

    'depends': ['base'],
    'application': True,
    'installable': True,

    'data':[
        'security/ir.model.access.csv',
        'views/estate_property_offer_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_views.xml',
        'views/res_users_views.xml',
        'views/estate_menus.xml'
    ],

    'demo':[
        'demo/estate_property_demo.xml',
        'demo/estate_property_offer_demo.xml'
    ],

    'license': 'AGPL-3'
}
