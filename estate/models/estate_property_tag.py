from odoo import models, fields


class estatepropertytag(models.Model):
    _name = "estate.property.tag"
    _description = "model for tags"
    _order = "name"
    _sql_constraints = [
        (
            "property_tag_uniq",
            "unique(name)",
            "A property_tag with the same name already exists in this. ",
        )
    ]
    name = fields.Char(string="tags", required=True)
    color = fields.Integer("Color Index")
