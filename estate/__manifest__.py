{
    'name': 'Real Estate Kapat',
    'version': '1.1',
    'summary': 'Module to Mangage Real Estate Property Listings',
    'website': 'https://www.odoo.com/app/estate',
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menus.xml',
        'views/estate_property_offer_views.xml',
    ],
    'application': True,
    'author': 'kapat-odoo',
    'license': 'LGPL-3',
}
