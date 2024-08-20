from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "This model stores the estate property tags"
    _order = "name"
    _sql_constraints = [
        ('unique_tag', 'UNIQUE (name)', 'all tags must have a unique name')
    ]

    name = fields.Char(required=True)
    description = fields.Text()
    color = fields.Integer()
