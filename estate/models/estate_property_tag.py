from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tag of estate property"
    _unique_name = models.Constraint("UNIQUE(name)", "The name must be unique")

    name = fields.Char(required=True)
