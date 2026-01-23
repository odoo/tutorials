from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "An estate property tag model"
    _order = "name asc"

    # === FIELDS ===#

    name = fields.Char(
        required=True)
    color = fields.Integer()

    _check_name = models.Constraint(
        'unique(name)',
        'The tag name must be unique!',
    )
