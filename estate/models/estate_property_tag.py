from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = "Estate Property Tag"
    _order = "name"

    name = fields.Char()
    property_ids = fields.Many2many('estate.property')
    color = fields.Integer()

    _unique_name = models.Constraint(
    'UNIQUE(name)',
    'name already exists!',
    )
