from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = "Estate Property Tag"

    name = fields.Char("Estate Property Tag", required=True)

    _check_unique_property_name = models.Constraint(
            'UNIQUE(name)',
            "The property name must be unique")
