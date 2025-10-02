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
        # models
        "models/x_real_estate_property_model.xml",
        "models/x_real_estate_property_offer_model.xml",
        "models/x_real_estate_property_type.xml",
        "models/x_real_estate_property_tag.xml",
        # fields
        "models/x_real_estate_property_offer_fields.xml",
        "models/x_real_estate_property_fields.xml",

        "security/ir.model.access.csv",

        "views/x_real_estate_property_type_views.xml",
        "views/x_real_estate_property_tag_views.xml",
        "views/x_real_estate_property_offer_views.xml",
        "views/x_real_estate_property_views.xml",
        "views/x_real_estate_menus.xml",
    ],
}
