{
    'name': 'Real Estate Kapat',
    'version': '1.1',
    'summary': 'Module to Mangage Real Estate Property Listings',
    'website': 'https://www.odoo.com/app/estate',
    'depends': [
        'base',
        'mail',
        'website',
        'whatsapp',
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/mass_offer_wizard_view.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_views.xml',
        'views/res_users_views.xml',
        'views/estate_menus.xml',
        'report/estate_property_templates.xml',
        'report/estate_property_reports.xml',
        'data/ir_cron_data.xml',
        'data/data.xml'
    ],
    'demo': [
        'data/estate_demo.xml',
    ],
    'application': True,
    'author': 'kapat-odoo',
    'license': 'LGPL-3',
}
