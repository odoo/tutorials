from odoo import models, fields


class EstatePropertyTags(models.Model):
    _name = "estate.property.tags"
    _description = "Estate Property Tags"
    _order = "name"
    name = fields.Char(required=True)
    color = fields.Integer(string="Color Index")
    _sql_constraints = [
        ("name_uniq", "unique(name)", "Tags must be unique"),
    ]
