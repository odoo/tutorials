from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property tags"

    _order = "name"

    _sql_constraints = [("unique_name", "UNIQUE(name)", "Tag names should be unique")]

    name = fields.Char(required=True)
    color = fields.Integer()
