from odoo import models, fields


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"

    # constraints
    _unique_tag = models.Constraint(
        'UNIQUE(name)',
        'Tag name should be unique'
    )

    name = fields.Char(string="Name", required=True)
