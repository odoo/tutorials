# Part of Odoo. See LICENSE file for full copyright and licensing details.  

{
    'name': "Estate",
    'category': "Real Estate/Brokerage",
    'summary': "Real Estate Advertisement Management",
    'version': "1.0",
    'author': "praj",
    'depends': ['base', 'website'],
    'data': [
        'report/estate_property_templates.xml',  
        'report/estate_property_reports.xml',  
        'security/security.xml',  
        'security/ir.model.access.csv',  
        'wizards/estate_property_offer_wizard_view.xml',  
        'views/estate_property_views.xml',  
        'views/estate_property_offer_views.xml',  
        'views/estate_property_type_views.xml',  
        'views/website_property_menu.xml',  
        'views/estate_property_list.xml',  
        'views/property_detail_template.xml',  
        'views/estate_property_tag_views.xml',  
        'views/estate_menus.xml',  
        'views/res_users.xml',  
        'data/estate_property_master_data.xml',  
        'demo/estate_property_demo_data.xml',   
    ],
    'installable': True,
    'application': True,
    'license': "LGPL-3"
}
