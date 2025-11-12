{
    'name':"Real Estate",
    'version': '0.1',
    'summary':"an application which helps every real estate business owner", 
    'description':"""
This module introduces a dedicated real estate management system, covering property listings,
detailed property information, and offer tracking. It provides a list view for properties and
a form view summarizing key details such as type and location. The module also enables sellers
to manage offers from potential buyers, allowing bids above or below the expected price.
    """,
    'author': "panj",
    'category': 'Real Estate/Brokerage',
    'website': "https://www.odoo.com",
    'depends': ['base', 'website', 'mail'],
    'data':[
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/estate_property_offer_views.xml',
        'wizard/estate_add_offers_wizard_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_type_views.xml',
        'views/res_users_views.xml',
        'views/estate_menus.xml',
        'views/estate_website_template.xml',
        'report/estate_property_reports.xml',
        'report/estate_property_templates.xml'
    ],
    'demo':[
        'demo/estate_property_demo.xml',
        'demo/estate_property_offer_demo.xml'
    ],
    'application': True,
    'installable': True,
    'license': 'AGPL-3'
}
