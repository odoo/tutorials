from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'

    name = fields.Char(string='Name', required=True, default="Unknown")

    _unique_type_name = models.Constraint(
        'unique (name)',
        'The name of a property type should be unique.',
    )
