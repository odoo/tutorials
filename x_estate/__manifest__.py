# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Estate (import)',
    'depends': [
        'base',
        'base_import_module',
    ],
    'version': '19.0.0.0',
    'author': "Odoo S.A.",
    'license': "LGPL-3",
    'installable': True,
    'application': True,
    'data': [
        "models/x_real_estate_property_type.xml",
        "models/x_real_estate_property.xml",
        "security/ir.model.access.csv",
        "views/x_real_estate_property_type_views.xml",
        "views/x_real_estate_property_views.xml",
        "views/x_real_estate_menus.xml",
    ],
}
