from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tags"

    _sql_constraints = [
        ("name_unique", "unique(name)", "Name must be unique!"),
    ]

    name = fields.Char(string="Tag", required=True)
