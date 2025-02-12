from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tags"
    _description = "Different Tags to describe the aesthetics of Property"
    _order = "name"

    name = fields.Char("Property Tag", required=True)
    color = fields.Integer("Color", default=1, help="Tag Color")
    _sql_constraints = [("name", "Unique(name)", "The tags should be unique")]
