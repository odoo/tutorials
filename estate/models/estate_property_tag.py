from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tags"

    _order = "name"

    name = fields.Char(required=True)

    color = fields.Integer()

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'The property tag must be unique!'),
    ]