from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tags"
    _order = "name"

    name = fields.Char(string="Tag", required=True)
    color = fields.Integer("Color Index", default=0, help="Color index for the tag")

    _sql_constraints = [
        ('check_name', 'UNIQUE(name)', 'A tag must be unique.'),
    ]
