from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real-estate property tag"
    _order = "name"

    _sql_constraints = [("name_unique", "UNIQUE(name)", "Property Tag already exists.")]

    name = fields.Char(required=True)
    color = fields.Integer()
