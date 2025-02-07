from odoo import fields, models

class estatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate property Tag"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Char(string="Color", default="#FFFFFF")  # Store HEX values

    _sql_constraints = [
          ("unique_property_tag", "UNIQUE(name)",
          "A property tag must be unique")
    ]