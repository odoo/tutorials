from odoo import fields, models


class estatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "This module introduces property tags to the real estate model, allowing properties to be categorized with multiple descriptive tags like 'cozy' or 'renovated' using a many-to-many relationship."

    name = fields.Char("Name", required=True)
