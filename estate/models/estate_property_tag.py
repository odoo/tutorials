from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "this is defind the tag of properties"
    _order = "name"

    name = fields.Char("Property tags", required=True)
    color = fields.Integer()

    _check_unique_tag = models.Constraint("UNIQUE(name)", "The Tag must be Unique")
