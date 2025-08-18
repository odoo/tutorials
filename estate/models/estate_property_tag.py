from odoo import fields, models


class estate_Property_Tag(models.Model):
    _name = "estate.property.tag"
    _description = "relevent tags"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer("Color", default=0)

    _sql_constraints = [
        ('check_tag_name', 'UNIQUE(name)', 'The name must be unique.')
    ]
