from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tags"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()
    _unique_price = models.Constraint(
        "UNIQUE(name)", "Property tag must be unique.")
