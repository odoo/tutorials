from odoo import fields, models


class PropertyTag(models.Model):
    _name = "real.estate.property.tag"
    _description = "Property Type"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()

    _sql_constraints = [("name", "UNIQUE(name)", "A property tag name must be unique")]
