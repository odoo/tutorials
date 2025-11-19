# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'

    name = fields.Char(string='Property Type', required=True)

    _type_name_uniq = models.Constraint(
        'unique(name)',
        "The property type name must be unique",
    )
