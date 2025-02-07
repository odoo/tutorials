from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tags"
    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', "Tag name must be unique!")
    ]

    name = fields.Char("Tag Name", required=True, help="Property Tags")
    