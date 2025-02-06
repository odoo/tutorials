# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Contains all property type"

    name = fields.Char(string="Property Type", required=True)
