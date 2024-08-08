from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"

    name = fields.Char(string='Name', required=True)

    _sql_constraints = [
        ('name_uniq', 'unique(name)',
        'A tag with the same name already exists')
    ]
