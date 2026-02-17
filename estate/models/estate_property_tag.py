from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"

    name = fields.Char(string="Tag Name", required=True)

    _unique_name = models.Constraint(
        "UNIQUE(name)", "The property tag name must be unique."
    )
