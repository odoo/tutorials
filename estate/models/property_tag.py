from odoo import models, fields


class PropertyTag(models.Model):
    _name = "real.estate.property.tag"
    _description = "Property Type"

    name = fields.Char(required=True)

    _sql_constraints = [("name", "UNIQUE(name)", "A property tag name must be unique")]
