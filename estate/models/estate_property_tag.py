from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Type"

    name = fields.Char(required=True, string="Name")
    