from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag Model"
    _order = "name"

    name = fields.Char(string='Tags', required=True)
    color = fields.Integer(string='color')

    _sql_constraints = [
        ('unique_tags_name', 'UNIQUE(name)', 'Tag name must be unique.'),
    ]
