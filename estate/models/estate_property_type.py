# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"

    name = fields.Char(string="Property Type", required=True)
