from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tag for estate properties"
    _order = "name"

    name = fields.Char('Name', required=True, translate=True)
    color = fields.Integer('Color', default=1)

    _unique_name = models.Constraint('UNIQUE(name)', 'Tag name must be unique.')
