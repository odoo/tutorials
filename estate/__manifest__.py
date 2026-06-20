{
    'name': 'Estate',
    'version': '1.0',
    'summary': 'Tutorial module for managing real estate properties',
    'description': 'A starter module to learn Odoo development by managing estate properties.',
    'author': '',
    'depends': ['base'],
    'data': [
        "views/estate_property_offer.xml",
        "views/estate_property_type.xml",
        "views/estate_property_tag.xml",
        "views/estate_property.xml",
        "security/ir.model.access.csv"
    ],
    'installable': True,
    'application': True,
}
