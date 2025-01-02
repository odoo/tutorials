from odoo import models, fields


class EstatePropertyTags(models.Model):
    _name = "estate.property.tags"
    _description = "Estate Property Tags"

    name = fields.Char(required=True)
    _sql_constraints = [
        ("name_uniq", "unique(name)", "Tags must be unique"),
    ]
