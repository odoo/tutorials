from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag Model"
    _order = 'name'

    name = fields.Char('Name', required=True)
    color = fields.Integer('Color')

    _sql_constraints = [
        ('check_tag_name', 'UNIQUE(name)', 'Tag Name must be unique.'),
    ]
