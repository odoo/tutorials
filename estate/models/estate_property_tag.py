from odoo import models, fields


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"

    name = fields.Char(string="Name", required=True)

    _check_unique_name = models.Constraint(
        'UNIQUE(name)',
        "The tag name must be unique."
    )
