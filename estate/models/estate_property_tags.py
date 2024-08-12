from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"

    name = fields.Char(string='Name', required=True)
    color = fields.Integer('Color Index')

    _sql_constraints = [
        ('name_uniq', 'unique(name)',
        'A tag with the same name already exists')
    ]
