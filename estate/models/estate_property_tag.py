from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property tag"
    name = fields.Char(required=True)
    _unique_name = models.Constraint("UNIQUE(name)", "Tag names must be unique")
