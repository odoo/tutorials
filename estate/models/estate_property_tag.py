from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag Model"
    _order = "name"

    name = fields.Char("Tag Name", required=True)
    color = fields.Integer()

    # Constraints
    _unique_name = models.Constraint("UNIQUE(name)", "Property Tag name must unique!")
