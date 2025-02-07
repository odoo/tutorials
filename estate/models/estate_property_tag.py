# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Contains all property tags"

    name = fields.Char(string="Property Tag", required=True)
