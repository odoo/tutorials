from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate_property_tag"
    _description = "this is defind the tag of properties"

    name = fields.Char("Property tags", required=True)
    _check_unique_tag = models.Constraint("UNIQUE(name)", "The Tag must be Unique")
