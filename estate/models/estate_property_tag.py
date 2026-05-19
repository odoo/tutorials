from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Real Estate Property Tag'
    _order = 'name'
    _check_name_uniq = models.Constraint(
        'unique (name)',
        'Each tag name must be unique.',
    )

    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color")
