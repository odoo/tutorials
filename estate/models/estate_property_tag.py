from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag Model"
    _order = "name"

    name = fields.Char(
        string="Property Tag",
        required=True)
    color = fields.Integer()

    _check_name_unique = models.Constraint("UNIQUE(name)", "Tag must be unique.")
