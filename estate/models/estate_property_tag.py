from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'
    _order = 'name'

    name = fields.Char(string='Name', required=True, default="Unknown")
    color = fields.Integer(string='Color')

    _unique_tag_name = models.Constraint(
        'unique (name)',
        'The name of a property tag should be unique.',
    )
