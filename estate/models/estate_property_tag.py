from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tag for the property of the estate module"

    name = fields.Char(required=True)
    property_ids = fields.Many2many("estate.property", string="Properties")
