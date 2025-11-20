from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"

    name = fields.Char("Name", required=True)

    _tag_name_unique = models.Constraint("UNIQUE(name)")
