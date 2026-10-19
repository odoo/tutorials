from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "this model is used to define tags to the properties"
    _order = "name"

    name = fields.Char(string="Tags")
    color = fields.Integer("Color Index", default=0)

    _check_name = models.Constraint(
        "unique(name)", "The name of the property tag name must be unique"
    )
