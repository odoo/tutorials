from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property.tag"
    _description = "EstatePropertyTag"
    _order = "name"

    # created the fields for the estate.property.tag model
    name = fields.Char(required=True)
    color = fields.Integer(string="Color Index")

    # created the Sql constraints for unique tags
    _sql_constraints = [
        ("unique_name", "unique(name)", "A property tag name must be unique.")
    ]
