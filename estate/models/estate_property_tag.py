from odoo import fields, models


class EstatePropertyTag(models.Model):

    _name = "estate.property.tag"
    _description = "estate property tag"
    _order = "id"
    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'the tag name must be unique')
    ]

    name = fields.Char("Name", required=True)
