from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"

    name = fields.Char(string="Name", required=True)

    _check_unique_tag_name = models.Constraint(
        "UNIQUE(name)", "The property tag name must be unique"
    )
