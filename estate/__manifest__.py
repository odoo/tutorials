{
    'name': 'Estate',
    'category': 'Real Estate',
    'sequence': 1,
    'summary': 'Making the real estate app from tutorials',
    'website': 'www.odoo.com',
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_properties_view.xml',
        'views/estate_property_offer_view.xml',
        'views/estate_property_type_view.xml',
        'views/estate_property_tag_view.xml',
        'views/estate_menus.xml',
    ],
    'installable': True,
    'application': True,
    'author': 'Rini Pillai',
    'license': 'LGPL-3',
}
