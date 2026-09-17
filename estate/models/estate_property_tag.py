from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'

    name = fields.Char(string='Name', required=True, default="Unknown")

    _unique_tag_name = models.Constraint(
        'unique (name)',
        'The name of a property tag should be unique.',
    )
