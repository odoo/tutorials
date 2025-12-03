from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = "Estate Property Tag"

    _order = 'name'

    name = fields.Char("Estate Property Tag", required=True)
    color = fields.Integer()

    _check_unique_property_name = models.Constraint(
            'UNIQUE(name)',
            "The property name must be unique")
