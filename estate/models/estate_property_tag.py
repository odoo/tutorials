from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate property tag"
    _order = "name"

    _unique_name = models.Constraint("UNIQUE (name)", "A tag should be unique")

    name = fields.Char(required=True)
    color = fields.Integer()
