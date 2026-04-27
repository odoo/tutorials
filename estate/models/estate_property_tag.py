from odoo import models, fields


class PropertyTag(models.Model):
    # Private attributes
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'
    _order = 'name'

    # Field declarations
    name = fields.Char(required=True)
    color = fields.Integer()

    # SQL constraints and indexes
    _check_name = models.Constraint(
        "unique(name)", "Tag name should be unique"
    )
