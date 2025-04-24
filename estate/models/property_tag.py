# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models


class PropertyTag(models.Model):
    _name = "property_tag"
    _description = "Property Tag Model"
    name = fields.Char(required=True)
